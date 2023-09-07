FROM python:3.11.4-alpine3.18

WORKDIR /app
RUN apk add python3-dev build-base linux-headers pcre-dev

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY mongoFlask.py .

CMD ["uwsgi", "--http", "127.0.0.1:8000", "--wsgi-file", "./mongoFlask.py", "--callable", "app"]