FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY crawler.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -u test_crawler.py

CMD [ "python", "-u", "./crawler.py" ]