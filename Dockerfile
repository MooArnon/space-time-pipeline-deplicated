FROM python:3.9

WORKDIR /app

COPY requirements.txt requirements.txt
COPY rest_api.py rest_api.py

RUN pip install --no-cache-dir --upgrade -r requirements.txt

EXPOSE 8000

CMD [ "uvicorn", "api.rest_api:app", "--host", "0.0.0.0", "--port", "8000" ]