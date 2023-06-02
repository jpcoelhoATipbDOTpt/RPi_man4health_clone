#! /usr/bin/python3

import paho.mqtt.client as mqttclient
import time
import json
import serial, string

flag = 0

# Inicializa puerto Serial
ser = serial.Serial('/dev/ttyUSB0',9600,8,'N',1, write_timeout = 1)
time.sleep(2)

flag = 0
#print("+++")
ser.write(b'R\r\n')
time.sleep(1)

def on_connect(client, usedata,flags,rc):
    if rc==0:
        print("Client ligado")
        global connected
        connected=True
    else:
        print("Falha de ligação do cliente")
        
# Configuración MQTT
connected = False
broker_address = "193.136.195.25"
port = 1883
client = mqttclient.Client("MQTT")
client.on_connect = on_connect

# MQTT Topic
apikey = "Meteo"
deviceid = "Pluviometro"
protocol = "json"
topic = "/" + protocol +"/" + apikey + "/" + deviceid + "/attrs"

# Lectura de los Datos
#print("---")	
ser.write(b'R\r\n')
time.sleep(5)
output = ser.readline()
time.sleep(5)
print (output)
array_out = output.split()
print(array_out)

# Verifica que haya almacenado todos los elementos, sino, vuelve a realizar la lectura del puerto
while flag == 0:
	if len(array_out) != 12:
		ser.write(b'\r\n')
		time.sleep(1)
		print("No tiene 12 elementos\n")
		ser.write(b'R\r\n')
		time.sleep(5)
		output = ser.readline()
		time.sleep(5)
		print(output)
		array_out = output.split()
		print(array_out)
	else:
		#print("Si tiene 12 elementos\n")
		flag = 1

# Guarda las variables a enviar
ACC = array_out[1]
EVENT_ACC = array_out[4]
TOTAL_ACC = array_out[7]
R_INT = array_out[10]

# Muestra los valores (para debug)
print("El Acumulado es:", ACC.decode(),"mm")
print("El Evento Acumulado es:", EVENT_ACC.decode(),"mm")
print("El Total Acumulado es:", TOTAL_ACC.decode(),"mm")
print("El R Int es:", R_INT.decode(),"mmph")


# Crea el payload en formato json
payload = {"AC": ACC.decode(),
           "EA": EVENT_ACC.decode(),
           "TA": TOTAL_ACC.decode(),
           "RI": R_INT.decode() }

message = json.dumps(payload)
print(message)

# Publicar datos en el broker
try:
    client.connect(broker_address,port=port)
    
    client.loop_start()
    
    while connected != True:
        time.sleep(0.2)
        
    client.publish(topic,message)
    client.loop_stop()
except:
    print("Imposible conectar al broker MQTT ")
