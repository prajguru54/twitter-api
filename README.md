# news-api
This simple repo demonstrates a simple web app through which we can search news on the basis of any keyword

### Running Locally using pip
1. python -m venv venv
2. source venv/bin/activate
1. pip install -r requirements.txt
2. uvicorn user_service.main:app --reload

### Running Locally using poetry
1. poetry install
2. source .venv/bin/activate
3. uvicorn user_service.main:app --reload

