import fastapi
from minio import Minio
import easyocr
import requests
import json

api = fastapi.FastAPI()
minio_client = client = Minio("your minio url", access_key='kontorskii', secret_key='your_secret_key', secure=False)
reader = easyocr.Reader(['ru'], gpu = True)

@api.get('/ocr')
def ocr(bucket:str, file: str):
    download = minio_client.fget_object(bucket, file, file)
    return asyncio.create_task(perform_text_recognition(bucket, file))    
    

async def perform_text_recognition(bucket: str, file: str):
    result = reader.readtext(file, detail = 0)
    response = ""
    for line in result:
        response += line
    
    payload = {
    'model': 'gemma3:4b',
    'prompt': 'Отформатируй текст и исправь в нем ошибки в словах, затем сгенерируй JSON с главной информацией из этого текста, пришли в ответе только этот JSON ' + response,
    'format': 'json',
    'keep-alive': '30m',
    'stream':  False
    }

    response = requests.post('YOUR_LLAMA_URL/api/generate', json=payload)
    minio_client.put_object()
    print(response)
    requests.post("YOUR_BACKEND_URL", json=json.loads(response))
    return response

