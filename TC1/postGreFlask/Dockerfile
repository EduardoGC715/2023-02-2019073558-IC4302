FROM python:3.11-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential

RUN pip install -U pip

COPY requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

COPY postgreFlask.py .

CMD [ "python", "-u", "./postgreFlask.py" ]