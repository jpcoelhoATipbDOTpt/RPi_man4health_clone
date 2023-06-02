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
        print("Client ligado")
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
deviceid = "SenseCAP01"
protocol = "json"
topic = "/" + protocol +"/" + apikey + "/" + deviceid + "/attrs"

# Configuração Modbus
PORT='/dev/SenseCAPdongle'
TEMP_REGISTER = 0
HUM_REGISTER  = 1
BAR_REGISTER  = 2
LUX_REGISTER  = 4

SLAVE_ADDRESS = 14

# Configura instrumento
instrument = minimalmodbus.Instrument(PORT,SLAVE_ADDRESS,mode=minimalmodbus.MODE_RTU)

# Parametros do instrumento
instrument.serial.baudrate = 9600        # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = None          # seconds

# Fecha porto
instrument.close_port_after_each_call = True
instrument.clear_buffers_before_each_transaction = True

# Le temperatura
airTemperature = instrument.read_register(TEMP_REGISTER,2,3,True)
# Le Humidade
airMoisture = instrument.read_register(HUM_REGISTER2,3,True)
# Le Pressão Atmosférica
MSW = instrument.read_long(BAR_REGISTER,3,True,3)
atmosphericPressure= (MSW*0.01)
# Le intensiade de radiação solar
MSW = instrument.read_long(LUX_REGISTER,3,True,3)
solarIlluminance= (MSW*0.01)
solarIrradiance = round(solarIlluminance * 0.008197,2)

# Mostra valores (debug apenas) 
print('The Air Temperature is: %.1f ºC\r' % airTemperature)
print('The Air Humidity is: %.1f percent\r' % airMoisture)
print('The Atmospheric Pressure is: %.1f Pa\r' % atmosphericPressure)
print('The Light Intensity is: %.1f lux\r' % solarIlluminance)
print('The Solar Irradiance is: %.1f W/m2\r' % solarIrradiance)

# Criar payload json

payload = {"AT": airTemperature,
           "AM": airMoisture,
           "AP": atmosphericPressure,
           "SI": solarIlluminance,
           "SR": solarIrradiance }


message = json.dumps(payload)

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
    
