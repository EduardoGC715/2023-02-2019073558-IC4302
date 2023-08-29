FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY flask.py .
COPY requirements.txt .
COPY templates .
COPY static .

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "-u", "./controller.py" ]