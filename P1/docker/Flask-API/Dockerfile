FROM python:3.11-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY apiFlask.py .
COPY logs ./logs
COPY bibliotec-98a06-firebase-adminsdk-qiahh-ea76f83463.json .

EXPOSE 5000

EXPOSE 8000

CMD [ "python", "-u", "./apiFlask.py" ]