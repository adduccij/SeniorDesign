# -*- coding: utf-8 -*-

"""
    Run.py
    Carriots.com
    Created 08 Oct 2016
"""

#!/usr/bin/python
from urllib2 import urlopen, Request
from json import dumps, loads
import RPi.GPIO as GPIO
import json

GPIO_pin = 4
ON = 'ON'
OFF = 'OFF'


class Carriots (object):
    api_url = "http://api.carriots.com/"

    def __init__(self, account, api_key, client_type='json'):
        self.client_type = client_type
        self.api_key = api_key
        self.account = account
        self.content_type = "application/vnd.carriots.api.v2+%s" % self.client_type
        self.headers = {'User-Agent': 'Raspberry-Carriots',
                        'Content-Type': self.content_type,
                        'Accept': self.content_type,
                        'Carriots.apikey': self.api_key}
        self.payload = None
        self.response = None

    def set_device(self, device):
        self.device = device + "@" + self.account + "." + self.account

    def send_stream(self, data):
        payload = {"protocol": "v2", "device": self.device, "at": "now", "data":data}
        self.payload = dumps(payload)
        request = Request(self.api_url + "streams", self.payload, self.headers)
        self.response = urlopen(request)
        return self.response

    def get_value_property(self, key_property):
        self.payload = None
        request = Request(self.api_url + "devices/" + self.device, self.payload, self.headers)
        self.response = urlopen(request)
        return json.loads(self.response.read()).get("properties").get(key_property)


def main():
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(GPIO_pin, GPIO.OUT)

    # Carriots parameters
    account = 'iadducchio3'
    apikey = '2e21ae9016512659fd3f632de24600aeeda61e56870e01525a9f6ae5f8d9855b'
    device = 'defaultDevice@iadducchio3.iadducchio3'

    # Instance object Carriots
    carriots = Carriots(account, apikey)

    carriots.set_device(device)

    history_value_device = OFF

    print "\n> :: Welcome...\n"

    while True:
        value_device = carriots.get_value_property('state')  # In this example, we use 'state' text

        if value_device != history_value_device:
            if value_device == ON:
                GPIO.output(GPIO_pin, GPIO.HIGH)
            else:
                GPIO.output(GPIO_pin, GPIO.LOW)

            print "> Property value of device: " + str(value_device) + "\n"
            history_value_device = value_device


if __name__ == '__main__':
    main()

    