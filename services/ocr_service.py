from models.schemas.hack import OcrRequest, OcrResponse
import requests

class OcrService():
    def sent_ocr_request(self, request: OcrRequest) -> int:
        response = requests.get('http://192.168.88.253:8000/ocr?file=' + request.file + '&bucket=' + request.bucket)
        return response