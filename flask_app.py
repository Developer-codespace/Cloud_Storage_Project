from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from ai_utils import extract_text, generate_tags, generate_category

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

        # AI-based content analysis
        text_content = extract_text(file_path)
        tags_list = generate_tags(text_content)
        category = generate_category(file_path, text_content)

        # Additional metadata
        file_size = os.path.getsize(file_path)
        file_type = file.mimetype
        tags = ', '.join(tags_list)
        user_id = 1  # Static for now; can be replaced with session-based ID
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

        return jsonify({
            "message": "File uploaded and metadata saved successfully.",
            "filename": filename,
            "category": category,
            "tags": tags_list
        }), 200

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
