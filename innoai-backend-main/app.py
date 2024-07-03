import sys
import os

# 현재 파일의 디렉토리 경로를 기반으로 부모 디렉토리를 추가합니다.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))

from services.pdf_processing_service import process_pdf
from flask import Flask, request

app = Flask(__name__)

@app.route('/process_pdf', methods=['POST'])
def process_pdf_endpoint():
    pdf_path = request.json['pdf_path']
    process_pdf(pdf_path)
    return {"status": "success"}

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
