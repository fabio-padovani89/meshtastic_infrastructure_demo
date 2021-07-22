from json import dumps, loads

import paho.mqtt.client as mqtt_client


class MQTTInterface:

    def __init__(self, host=None, topic=None):
        self.client = None
        self.host = host
        self.topic = topic

    def connect(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print('Connected to MQTT Broker!')
            else:
                print('Failed to connect, return code %d\n', rc)

        self.client = mqtt_client.Client()
        self.client.on_connect = on_connect
        self.client.connect(self.host)
        self.client.loop_start()

    def subscribe(self, callback=None):
        def on_message(client, userdata, msg):
            if callback:
                message = loads(msg.payload.decode())
                callback(message)
            else:
                print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")

        self.client.subscribe(self.topic)
        self.client.on_message = on_message

    def publish(self, messages):
        self.client.publish(
            self.topic,
            dumps(messages)
        )
    
    def close(self):
        self.client.disconnect()
