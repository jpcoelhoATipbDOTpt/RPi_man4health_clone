import serial
import json
import paho.mqtt.client as mqttclient
import time

#.............................................................................................
# Configuração MQTT
#.............................................................................................
def on_connect(client, usedata,flags,rc):
    if rc==0:
        print("Cliente ligado")
        global connected
        connected=True
    else:
        print("Falha de ligação do cliente")
#.............................................................................................
connected = False
broker_address = sys.argv[1]
#broker_address = "broker.hivemq.com"
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
#.............................................................................................
class DadosInvalidos(Exception):
    pass
#.............................................................................................
#.............................................................................................
# Lê dados do pluviómetro
#.............................................................................................
try:
    ser = serial.Serial('/dev/RS232dongle',9600,8,'N',1,timeout=1) # inicializa porto série
    ser.write(b'R\r\n')                                # envia comando
    data = ser.readline()                              # lê os dados ou timeout
    ser.close()                                        # fecha porto série

    if len(data)>69:                                   # O número de carateres não deve
        raise DadosInvalidos                           # se superior a este limite
    #.............................................................................................
    # Parse da string
    data_parsed = ((((data.decode("utf-8"))).rstrip()).replace(" mm, ", ",")).replace(" mmph", "")
    parse = data_parsed.split(",");
    
    valor=[0,0,0,0];
    for inx,item in enumerate(parse):
        overparse = item.split("  ");
        valor[inx] = float(overparse[1]);
    #.............................................................................................
    # Preenche payload
    payload = {"AC": valor[0],
               "EA": valor[1],
               "TA": valor[2],
               "RI": valor[3]}
    
except:
    payload = {"AC": -1,
               "EA": -1,
               "TA": -1,
               "RI": -1}

#.............................................................................................
# Publicar dados no broker
#.............................................................................................
message = json.dumps(payload)
try:
    client.connect(broker_address,port=port)
    client.loop_start()
    while connected != True:
        time.sleep(0.2)
        
    client.publish(topic,message)
    client.loop_stop()
except:
    print("Impossível conetar ao broker MQTT ")

