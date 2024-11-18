
**REST API по расчёту стоимости страхования в зависимости от типа груза и объявленной стоимости.**


## Getting started
Clone repo
```
git clone <path_repo>
```
Create .env file and insert data
```
DATABASE_URL="postgresql+asyncpg://{user}:{password}@{host}:5432/insurance_api">
POSTGRES_USER="{user}"
POSTGRES_PASSWORD="{password}"
```


Run the application:
```
docker-compose up -d
```

API documentation :
- 127.0.0.1:8000/docs
- 127.0.0.1:8000/redoc

Examples urls:
-  curl -X 'GET' \
  'http://localhost:8000/calculate_insurance/?cargo_type=Glass&declared_value=1000&target_date=2020-07-01' \
  -H 'accept: application/json'

- curl -X 'POST' \
  'http://localhost:8000/upload_rates/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{  
    "2020-06-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.04"
        }
    ],
    "2020-07-01": [
        {
            "cargo_type": "Glass",
            "rate": "0.05"
        },
        {
            "cargo_type": "Other",
            "rate": "0.01"
        }
    ]
}'