# Credit Card Default ML Service

## Описание проекта

Production-like минималистичный сервис для прогнозирования дефолта по кредитным картам.  
Проект включает:
- обучение модели RandomForestClassifier;
- Flask API с эндпоинтами `/health` и `/predict`;
- контейнеризацию через Docker;
- базовые тесты;
- план A/B-тестирования.

Датасет: Default of Credit Card Clients Dataset с UCI / Kaggle.

## Структура проекта

```text
.
├── app/
│   ├── __init__.py
│   ├── api.py
│   └── model_handler.py
├── models/
│   ├── __init__.py
│   ├── train.py
│   └── artifacts/
│       ├── model.pkl
│       └── metadata.json
├── tests/
│   └── test_api.py
├── docker/
│   └── Dockerfile
├── screenshots/
│   ├── Dockerdesktop.png
│   ├── health.png
│   └── predict.png
├── download_data.py
├── docker-compose.yml
├── .dockerignore
├── .gitignore
├── ab_test_plan.md
├── requirements.txt
└── README.md
```

## Модель

Используется модель **RandomForestClassifier** для задачи бинарной классификации: предсказание дефолта клиента по кредитной карте.

Скрипт обучения:
```bash
python models/train.py
```

После обучения создаются артефакты:
- `models/artifacts/model.pkl`
- `models/artifacts/metadata.json`

## Локальный запуск

### 1. Установка зависимостей

```bash
python -m venv .venv
```

Windows PowerShell:
```powershell
.\.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Обучение модели

```bash
python models/train.py
```

### 3. Запуск API

```bash
python -m app.api
```

Сервис будет доступен по адресу:
```text
http://localhost:5000
```

## API

### GET /health

Проверка состояния сервиса и загрузки модели.

Пример запроса:
```powershell
Invoke-RestMethod -Uri http://localhost:5000/health -Method GET | ConvertTo-Json
```

Пример ответа:
```json
{
  "healthy": true,
  "model_version": "v1",
  "status": "ok"
}
```

### POST /predict

Принимает JSON с признаками клиента и возвращает:
- `prediction` — предсказанный класс (0/1);
- `probability` — вероятность дефолта;
- `model_version` — версия модели.

Пример запроса:
```powershell
Invoke-RestMethod `
  -Uri http://localhost:5000/predict `
  -Method POST `
  -ContentType "application/json" `
  -Body '{"LIMIT_BAL":20000,"SEX":2,"EDUCATION":2,"MARRIAGE":1,"AGE":34,"PAY_0":0,"PAY_2":0,"PAY_3":0,"PAY_4":0,"PAY_5":0,"PAY_6":0,"BILL_AMT1":3913,"BILL_AMT2":3102,"BILL_AMT3":689,"BILL_AMT4":0,"BILL_AMT5":0,"BILL_AMT6":0,"PAY_AMT1":0,"PAY_AMT2":689,"PAY_AMT3":0,"PAY_AMT4":0,"PAY_AMT5":0,"PAY_AMT6":0}' `
| ConvertTo-Json
```

Пример ответа:
```json
{
  "model_version": "v1",
  "prediction": 0,
  "probability": 0.27
}
```

## Тесты

Запуск тестов:
```bash
python -m pytest -q
```

## Docker

### Сборка образа

```bash
docker build -f docker/Dockerfile -t credit-default-service:latest .
```

### Запуск контейнера

```bash
docker run --rm -p 5000:5000 credit-default-service:latest
```

## Docker Compose

Запуск:
```bash
docker compose up --build
```

Остановка:
```bash
docker compose down
```

## Архитектура: монолит vs микросервисы

В рамках данного учебного проекта выбран **монолитный подход**.  
Причины:
- минимальная сложность для MVP;
- быстрее разработка и деплой;
- меньше операционных накладных расходов;
- достаточно для одного ML use-case.

Переход к микросервисной архитектуре будет оправдан при росте нагрузки, появлении нескольких моделей, разных SLA и необходимости независимого масштабирования компонентов.

## Логирование, мониторинг и MLOps-концепты

### RabbitMQ
В production-сценарии RabbitMQ можно использовать для:
- асинхронного batch scoring;
- retraining jobs;
- логирования и доставки событий в очередь.

### Логирование
API-запросы и ответы могут логироваться в JSON-формате с полями:
- `request_id`
- `latency`
- `model_version`
- `status_code`

В production такие логи могут централизованно собираться через ELK / OpenSearch / Grafana stack.

### DVC
DVC используется для контроля версий данных и ML-артефактов, а также для воспроизводимости пайплайна.

### MLflow
MLflow используется для трекинга экспериментов, хранения метрик, параметров и артефактов моделей.

## ONNX-ML, uWSGI и NGINX

### ONNX-ML
Модель scikit-learn можно преобразовать в ONNX-формат для ускоренного инференса и более удобного кросс-платформенного развёртывания.

### uWSGI + NGINX
В production среде:
- **uWSGI / Gunicorn** выступает как WSGI-сервер для Python-приложения;
- **NGINX** работает как reverse proxy, распределяет запросы, обрабатывает TLS, статику и балансировку нагрузки.

## Бизнес-метрики

Помимо технических метрик используются бизнес-метрики:
- **Expected loss reduction** — ожидаемое снижение потерь от дефолтов;
- **Approval rate at fixed risk** — доля одобренных заявок при фиксированном уровне риска.

## Демонстрация

Скриншоты работы сервиса находятся в папке `screenshots/`.

## Docker Hub

Ссылка на опубликованный Docker-образ:

```text
https://hub.docker.com/repository/docker/denlex92/credit-default-service
```
