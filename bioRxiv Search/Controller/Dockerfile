FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY controller.py .
COPY requirements.txt .
COPY test_controller.py .

RUN pip install --no-cache-dir -r requirements.txt

RUN python -u test_controller.py

CMD [ "python", "-u", "./controller.py" ]