import atexit
from os import environ

from flask import Flask
from flask_cors import CORS

from .db_interface import store_nodes_info

app = Flask(__name__)
CORS(app)

import web_server.views

from .mqtt import MQTTInterface


mqtt = MQTTInterface(
  host=environ.get('MQTT_HOST'),
  topic=environ.get('MQTT_IN_TOPIC')
)
mqtt.connect()
mqtt.subscribe(callback=store_nodes_info)


def exit_procedure():
  mqtt.close()

atexit.register(exit_procedure)