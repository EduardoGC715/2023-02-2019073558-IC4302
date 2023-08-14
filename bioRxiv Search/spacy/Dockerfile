FROM python:3.11-slim

WORKDIR /app

RUN apt-get update
RUN apt-get install -y build-essential


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY spacyentity.py .
CMD [ "python", "-u", "./spacyentity.py" ]