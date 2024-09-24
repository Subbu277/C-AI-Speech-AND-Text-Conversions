FROM python:3.10-slim

ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_RUN_PORT=8080
ENV google_api_key=

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080


CMD ["flask", "run"]

# Build : docker build -t my-flask-app .
# Run : docker run -p 8080:8080 my-flask-app
