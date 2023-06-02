#! /usr/bin/python3

"""
Created on Fri Sep 30 12:43:58 2022

@author: jpcoelho
"""

import minimalmodbus
import paho.mqtt.client as mqttclient
import time
import json

def on_connect(client, usedata,flags,rc):
    if rc==0:
        print("Cliente ligado")
        global connected
        connected=True
    else:
        print("Falha de ligação do cliente")
        
# Configuração MQTT
connected = False
# broker_address = "192.168.1.68"
broker_address = "193.136.195.25"
port = 1883
# user="man4health"
# password="#Man4Health"
client = mqttclient.Client("MQTT")
#client.username_pw_set(user,password=password)
client.on_connect = on_connect

## Tópico MQTT
apikey = "Meteo"
deviceid = "CO2DEV01"
protocol = "json"
topic = "/" + protocol +"/" + apikey + "/" + deviceid + "/attrs"

# Configuração Modbus
PORT='/dev/RS485dongle'
REGISTER = 8

SLAVE_ADDRESS = 69

# Configura instrumento
instrument = minimalmodbus.Instrument(PORT,SLAVE_ADDRESS,mode=minimalmodbus.MODE_RTU)

# Parametros do instrumento
instrument.serial.baudrate = 9600        # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 1          # seconds
instrument.precalculate_read_size= False
# Fecha porto
instrument.close_port_after_each_call = True
instrument.clear_buffers_before_each_transaction = True

# Le dados
try:
    dados = instrument.read_registers(REGISTER,3,3)
except:
    dados = [0,0,0]
    
# Mostra valores (debug apenas) 
# print(*dados, sep=",")

# Criar payload json

payload = { "AT": dados[1]/100, # Air Temperature   (ºC)
            "AM": dados[2]/100, # Air Moisture      (%)
           "CO2": dados[0]/10   # CO2 concentration (ppm)
           }


message = json.dumps(payload)
# Mostra valores (debug apenas) 
print(message)

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
