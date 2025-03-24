FROM registry.flowai.ru/base/python:3.12-slim
WORKDIR /app

COPY src/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt --root-user-action=ignore

COPY src /app/

EXPOSE 8080
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]

