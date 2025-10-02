# hackathon-back

## Запуск
### Общий (uvicorn)
    uvicorn main:app --host 127.0.0.1 --port 8000 --reload
### Linux only (gunicorn)
    gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000

#### Параметры
* w - кол-во воркеров. В доке написано, что должно быть от 2 до 4 воркеров на ядро сервера
## OpenAPI
http://127.0.0.1:8000/docs - при запущенном приложении постучать на роут docs
## Деплой через Docker

	docker compose up -d

	docker build -t hackathon-backend .
	
	docker run --network kontorskii-backend_default -p 8002:8002 --name hackathon-backend -d hackathon-backend

### Дополнительно
- admin/password
- propab/prorab
- goscont/goscont
