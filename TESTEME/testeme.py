#! /usr/bin/python3

"""
Created on Fri Sep 30 12:43:58 2022

@author: jpcoelho
"""
import sys
import minimalmodbus
import paho.mqtt.client as mqttclient
import time
import json

def on_connect(client, usedata,flags,rc):
    if rc==0:
        print("Client ligado")
        global connected
        connected=True
    else:
        print("Falha de ligação do cliente")
        
# Configuração MQTT
connected = False
broker_address = sys.argv[1]
# broker_address = "192.168.1.68"
#broker_address = "193.136.195.25"
port = 1883
# user="man4health"
# password="#Man4Health"
client = mqttclient.Client("MQTT")
#client.username_pw_set(user,password=password)
client.on_connect = on_connect

## Tópico MQTT
maintopic = "man4health"
apikey = "teste"
deviceid = "testedev1"
protocol = "json"
topic = "/" + protocol +"/" + apikey + "/" + deviceid + "/attrs"

payload = {
  "T1": 1.0,
  "T2": "OK"
}

message = json.dumps(payload)

# Publicar dados no broker
try:
    client.connect(broker_address,port=port)    
    client.loop_start()
    while connected != True:
        time.sleep(0.2)
    client.publish(topic,message)
    client.loop_stop()
except:
    print("Impossível conetar ao broker MQTT ")
