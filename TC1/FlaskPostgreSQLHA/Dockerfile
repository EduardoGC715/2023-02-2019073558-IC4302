FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY requirements.txt .

RUN pip install -U pip
RUN pip install --no-cache-dir -r requirements.txt

COPY FlaskPostgreSQLHA.py .

CMD [ "python", "-u", "./FlaskPostgreSQLHA.py" ]