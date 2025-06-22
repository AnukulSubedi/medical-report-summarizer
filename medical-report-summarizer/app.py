import os
from flask import Flask, request, jsonify
from ocr_utils import extract_text_from_file
import pytesseract
from PIL import Image
import openai
from model import model_inference
from dotenv import load_dotenv
from flask import render_template
 
load_dotenv()

UPLOAD_FOLDER = 'uploads'
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('upload.html')


@app.route('/uploads', methods=['POST'])
def ocr_image():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty file'}), 400

    # filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    # file.save(filepath)
    filepath = f"uploads/{file.filename}"
    file.save(filepath)

     # Add the print statement here to debug
    print(f"File successfully saved at: {filepath}")  # Logs the saved file path

    try:
        extracted_text = extract_text_from_file(filepath)
        analysis = model_inference(extracted_text)
        return jsonify({'extracted_text': extracted_text, 'analysis': analysis})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Starting OCR API ...")
    app.run(debug=True, port= 5050)
