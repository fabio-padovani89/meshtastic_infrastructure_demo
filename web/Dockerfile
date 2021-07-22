# syntax=docker/dockerfile:1
FROM python:3.8-alpine
WORKDIR /web-src

## ENVS

# other
ENV LOG_LEVEL=DEBUG

# flask
ENV FLASK_APP=web_server
ENV FLASK_ENV=production
ENV FLASK_RUN_PORT=8000
ENV FLASK_RUN_HOST=0.0.0.0

# mongo
ENV MONGO_URL=mongodb://mongo:27017/
ENV MONGO_DATABASE=nodes_tracker
ENV MONGO_COLLECTION=nodes
ENV MONGO_USERNAME=root
ENV MONGO_PASSWORD=password
# 7 days -> 60 * 60 * 24 * 7
ENV MONGO_NODES_EXPIRE_SECONDS=604800

# MQTT
ENV MQTT_HOST=mosquitto
ENV MQTT_IN_TOPIC=input_data

RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["flask", "run"]
