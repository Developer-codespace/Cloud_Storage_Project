async function uploadFiles() {
    const fileInput = document.getElementById('fileInput');
    const progressBar = document.getElementById('uploadProgress');
    const fileList = document.getElementById('fileDisplay');

    const files = fileInput.files;
    if (files.length === 0) {
        alert("Please select at least one file to upload.");
        return;
    }

    progressBar.value = 0;
    progressBar.max = files.length;

    for (let i = 0; i < files.length; i++) {
        const formData = new FormData();
        formData.append("file", files[i]);

        try {
            const response = await fetch("http://127.0.0.1:5000/upload", {
                method: "POST",
                body: formData
            });

            const result = await response.json();

            // Display success message
            console.log(result.message);

            // Add file to the UI list
            const listItem = document.createElement("li");
            listItem.textContent = files[i].name + " (Uploaded)";
            fileList.appendChild(listItem);
        } catch (error) {
            console.error("Error uploading file:", error);
            const listItem = document.createElement("li");
            listItem.textContent = files[i].name + " (Failed)";
            fileList.appendChild(listItem);
        }

        // Update progress
        progressBar.value = i + 1;
    }

    fileInput.value = ""; // Clear the input
}
