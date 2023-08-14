FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY controller.py .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./controller.py" ]