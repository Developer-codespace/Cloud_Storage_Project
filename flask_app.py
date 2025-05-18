from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
CORS(app)

# Setup uploads folder
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        # Get file from request
        file = request.files['file']
        if not file:
            return jsonify({"error": "No file uploaded"}), 400

        # Extract and secure filename
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        # Additional metadata
        file_size = os.path.getsize(file_path)
        file_type = file.mimetype
        category = request.form.get('category', 'Uncategorized')
        tags = request.form.get('tags', '[]')  # You can store as JSON string if needed
        user_id = 1  # Static or from session
        visibility = 'private'
        is_deleted = 0
        storage_location = 'Local'
        upload_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # Open DB connection
        db = MySQLdb.connect(
            host="localhost",
            user="root",
            passwd="Niladri@Das7",
            db="backup_system"
        )
        cursor = db.cursor()

        # Insert all metadata into the database
        sql = """
            INSERT INTO files (
                user_id, filename, category, tags, file_size, file_type, 
                file_path, storage_location, upload_time, visibility, is_deleted
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (
            user_id, filename, category, tags, file_size, file_type,
            file_path, storage_location, upload_time, visibility, is_deleted
        )

        cursor.execute(sql, values)
        db.commit()

        return jsonify({"message": "File uploaded and metadata saved successfully."}), 200

    except Exception as e:
        print("Upload error:", e)
        return jsonify({"error": str(e)}), 500

    finally:
        try:
            cursor.close()
            db.close()
        except:
            pass

@app.route('/')
def index():
    return "Flask server running..."

if __name__ == '__main__':
    app.run(debug=True)
