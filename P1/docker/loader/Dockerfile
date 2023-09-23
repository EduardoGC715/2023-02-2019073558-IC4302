FROM python:3.11-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential

COPY requirements.txt .
COPY loader.py .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./loader.py" ]