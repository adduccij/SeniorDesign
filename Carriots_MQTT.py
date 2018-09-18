#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Client paho-mqtt CarriotsMqttServer
# main.py
import paho.mqtt.publish as publish
from json import dumps
from ssl import PROTOCOL_TLSv1



class CarriotsMqttClient():
    host = 'mqtt.carriots.com'
    port = 1883
    auth = {}
    topic = '%s/streams'
    tls = None


    def __init__(self, auth, tls=None):
        self.auth = auth
        self.topic = '%s/streams' % auth['username']
        if tls:
            self.tls = tls
            self.port = 8883


    def publish(self, msg):
        try:
            publish.single(topic=self.topic, payload=msg, hostname=self.host, auth=self.auth, tls=self.tls, port=self.port)
        except Exception as ex:
            print(ex)


if __name__ == '__main__':
    auth = {'username': '2e21ae9016512659fd3f632de24600aeeda61e56870e01525a9f6ae5f8d9855b', 'password': '1224iaUC'}
    print(auth)
    # tls_dict = {'ca_certs': 'ca_certs.crt', 'tls_version': PROTOCOL_TLSv1}  # ssl version
    msg_dict = {'protocol': 'v2', 'device': 'defaultDevice@iadducchio3.iadducchio3', 'at': 'now', 'data': {'temp': 21, 'hum':58}}
    client_mqtt = CarriotsMqttClient(auth=auth)                     # non ssl version
    # client_mqtt = CarriotsMqttClient(auth=auth, tls=tls_dict)      # ssl version
    client_mqtt.publish(dumps(msg_dict))