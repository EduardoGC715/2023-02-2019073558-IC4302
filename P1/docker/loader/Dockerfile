FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY requirements.txt .
COPY loader.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./loader.py" ]