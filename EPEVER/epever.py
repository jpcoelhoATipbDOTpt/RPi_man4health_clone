#! /usr/bin/python3

"""
16/outubro/2022
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
broker_address = "193.136.195.25" # Servidor IPB
# broker_address = "mrmaldoror.hopto.org"
# broker_address = "localhost"
port = 1883
# user="man4health"
# password="#Man4Health"
client = mqttclient.Client("MQTT")
#client.username_pw_set(user,password=password)
client.on_connect = on_connect

## Tópico MQTT
apikey = "Epever"
deviceid = "TracerA1210AL01"
protocol = "json"
topic = "/" + protocol +"/" + apikey + "/" + deviceid + "/attrs"
        
# Configuração Modbus
PORT='/dev/EPEVERdongle'

# Endereços
PV_IN_VOLTAGE_REG = 0x3100
PV_IN_CURRENT_REG = 0x3101
PV_IN_POWER_REG   = 0x3102 # L + H
LOAD_VOLTAGE_REG  = 0x310C
LOAD_CURRENT_REG  = 0x310D
LOAD_POWER_REG    = 0x310E # L + H
BAT_TEMP_REG      = 0x3110
DEV_TEMP_REG      = 0x3111
BAT_CAPACITY_REG  = 0x311A
BAT_REAL_VOLT_REG = 0x311D 
BAT_STATUS_REG    = 0x3200
CHARG_STATUS_REG  = 0x3201
DCHARG_STATUS_REG = 0x3202
MAX_BAT_V_DAY_REG = 0x3302
MIN_BAT_V_DAY_REG = 0x3303
EGY_COSMD_DAY_REG = 0x3304 # L + H 
EGY_COSMD_MTH_REG = 0x3306 # L + H
EGY_COSMD_YAR_REG = 0x3308 # L + H
EGY_COSMD_TOT_REG = 0x330A # L + H
EGY_GENTD_DAY_REG = 0x330C # L + H 
EGY_GENTD_MTH_REG = 0x330E # L + H 
EGY_GENTD_YAR_REG = 0x3310 # L + H 
EGY_GENTD_TOT_REG = 0x3312 # L + H 
BAT_MEAS_VOLT_REG = 0x331A
BAT_MEAS_CURT_REG = 0x331B # L + H 

SLAVE_ADDRESS = 1

# Configura instrumento
instrument = minimalmodbus.Instrument(PORT,SLAVE_ADDRESS,mode=minimalmodbus.MODE_RTU)

# Parametros do instrumento
instrument.serial.baudrate = 115200        # Baud
instrument.serial.bytesize = 8
instrument.serial.parity   = minimalmodbus.serial.PARITY_NONE
instrument.serial.stopbits = 1
instrument.serial.timeout  = 0.5          # seconds
# print(instrument)

# Fecha porto
instrument.close_port_after_each_call = True
instrument.clear_buffers_before_each_transaction = True

# PV array input voltage
PVarrayInputVoltage = instrument.read_register(PV_IN_VOLTAGE_REG,2,4,True)
# PV array input current
PVarrayInputCurrent = instrument.read_register(PV_IN_CURRENT_REG,2,4,True)
# PV array input power
MSW = instrument.read_long(PV_IN_POWER_REG,4,True,3)
PVarrayInputPower= (MSW*0.01)
# Load voltage
loadVoltage = instrument.read_register(LOAD_VOLTAGE_REG,2,4,True)
# Load current
loadCurrent = instrument.read_register(LOAD_CURRENT_REG,2,4,True)
# Load power
MSW = instrument.read_long(LOAD_POWER_REG,4,True,3)
loadPower= (MSW*0.01)
# Battery temperature
batteryTemperature = instrument.read_register(BAT_TEMP_REG,2,4,True)
# Device temperature
deviceTemperature = instrument.read_register(DEV_TEMP_REG,2,4,True)
# Battery SOC
batterySOC = instrument.read_register(BAT_CAPACITY_REG,2,4,True)
# Battery's real rated voltage
batteryRealRatedVoltage = instrument.read_register(BAT_REAL_VOLT_REG,2,4,True)
# Battery status
batteryStatus = instrument.read_register(BAT_STATUS_REG,2,4,True)
# Charging equipment status
chargingEquipmentStatus = instrument.read_register(CHARG_STATUS_REG,2,4,True)
# Discharging equipment status
dischargingEquipmentStatus = instrument.read_register(DCHARG_STATUS_REG,2,4,True)
# Maximum battery voltage today
maximumBatteryVoltageToday = instrument.read_register(MAX_BAT_V_DAY_REG,2,4,True)
# Minimum battery voltage today
minimumBatteryVoltageToday = instrument.read_register(MIN_BAT_V_DAY_REG,2,4,True)
# Consumed energy today
MSW = instrument.read_long(EGY_COSMD_DAY_REG,4,True,3)
consumedEnergyToday= (MSW*0.01)
# Consumed energy today
MSW = instrument.read_long(EGY_COSMD_DAY_REG,4,True,3)
consumedEnergyToday= (MSW*0.01)
# Consumed energy this month
MSW = instrument.read_long(EGY_COSMD_MTH_REG,4,True,3)
consumedEnergyMonth= (MSW*0.01)
# Consumed energy this year
MSW = instrument.read_long(EGY_COSMD_YAR_REG,4,True,3)
consumedEnergyYear= (MSW*0.01)
# Total consumed energy
MSW = instrument.read_long(EGY_COSMD_TOT_REG,4,True,3)
totalConsumedEnergy = MSW
# Generated energy today
MSW = instrument.read_long(EGY_GENTD_DAY_REG,4,True,3)
generatedEnergyToday= (MSW*0.01)
# Generated energy this month
MSW = instrument.read_long(EGY_GENTD_MTH_REG,4,True,3)
generatedEnergyMonth= (MSW*0.01)
# Generated energy this year
MSW = instrument.read_long(EGY_GENTD_YAR_REG,4,True,3)
generatedEnergyYear= (MSW*0.01)
# Total generated energy
MSW = instrument.read_long(EGY_GENTD_TOT_REG,4,True,3)
totalGeneratedEnergy= (MSW*0.01)
# Battery voltage
batteryVoltage = instrument.read_register(BAT_MEAS_VOLT_REG,2,4,True)
# Battery current
MSW = instrument.read_long(BAT_MEAS_CURT_REG,4,True,3)
batteryCurrent= (MSW*0.01)

# Mostra valores (debug apenas) 
print('The Device Temperature is: %.1f ºC\r' % deviceTemperature)
print('The Battery Voltage is: %.1f V\r' % batteryVoltage)

# Criar payload json

payload = { "A3": PVarrayInputVoltage,
            "A4": PVarrayInputCurrent,
            "A5": PVarrayInputPower,
            "A7": loadVoltage,
            "A8": loadCurrent, 
            "A9": loadPower,
            "A11": batteryTemperature,
            "A12": deviceTemperature,
            "A13": batterySOC,
            "A14": batteryRealRatedVoltage, 
            "A15": batteryStatus,
            "A16": chargingEquipmentStatus,
            "A17": dischargingEquipmentStatus,
            "A18": maximumBatteryVoltageToday,
            "A19": minimumBatteryVoltageToday,                      
            "A20": consumedEnergyToday,
            "A22": consumedEnergyMonth,
            "A24": consumedEnergyYear,
            "A26": totalConsumedEnergy,
            "A28": generatedEnergyToday,            
            "A30": generatedEnergyMonth,
            "A32": generatedEnergyYear,
            "A34": totalGeneratedEnergy,
            "A36": batteryVoltage,
            "A37": batteryCurrent
           }

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
    
