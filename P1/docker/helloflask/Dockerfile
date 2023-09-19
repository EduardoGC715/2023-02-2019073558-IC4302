FROM arm64v8/python:3.11.5-slim-bullseye

EXPOSE 5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY app/. .
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "flask",  "--app", "app", "run", "--host=0.0.0.0" ]
