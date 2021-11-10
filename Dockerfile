#https://cloud.google.com/run/docs/quickstarts/build-and-deploy/python
FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True
ENV APP_HOME /app
ENV PORT=8090
WORKDIR $APP_HOME
COPY . ./

RUN pip install --no-cache-dir -r requirements.txt

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app