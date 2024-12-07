from flask import Flask, request, jsonify, send_file
import pdfplumber
import pandas as pd
import os

app = Flask(__name__)
UPLOAD_FOLDER = "/path/to/your/hostinger/uploads"  # Update with your file manager path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Extract tables using pdfplumber
        extracted_data = []
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                extracted_data.extend(tables)

        # Save to Excel
        df = pd.DataFrame(extracted_data)
        excel_path = os.path.join(UPLOAD_FOLDER, 'converted.xlsx')
        df.to_excel(excel_path, index=False)

        return jsonify({"message": "File processed successfully", "download_url": excel_path})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
