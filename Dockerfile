FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install fastapi uvicorn python-multipart

EXPOSE 8000

CMD ["uvicorn", "unzip_api:app", "--host", "0.0.0.0", "--port", "8000"]