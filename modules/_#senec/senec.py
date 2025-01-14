#!/usr/bin/python

import struct
import json
import urllib2
import time
import paho.mqtt.client as mqttClient

LWT = "LWT"
debug = False
writing_in_file = False
writing_mqtt = True

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        # client.publish(mqtt_topic+LWT,payload="Online", qos=0, retain=True)
        if debug:
            print("Connected to Broker")
    else:
        print("Connection to Broker failed")

broker_address = "192.168.178.21"
port = 1883

client = mqttClient.Client("Python-openWB-SENEC")  # create new instance
client.on_connect = on_connect  # attach function to callback
# client.will_set(mqtt_topic+LWT, payload="Offline", qos=0, retain=True)
client.connect(broker_address, port=port)  # connect to broker
if debug:
    print("Trying to connect MQTT-Broker")
client.loop_start()  # start the loop


ipaddress = "192.168.178.56"

#ipaddress = str(sys.argv[1])


def myDecode(stringValue):
# Parameter: 
# stringValue:	String Wert, im Format Typ_Wert 
# 
# Rueckgabe:
# result: 		Floatzahl
    splitValue = stringValue.split('_')

    if splitValue[0] == 'fl':
        #Hex >> Float
        result = struct.unpack('f',struct.pack('I',int('0x'+splitValue[1],0)))[0]
    elif splitValue[0] == 'u3': 
        pass #TBD
    elif splitValue[0] == 'u8':
        pass #TBD
    
    return result

def writeVal(filePath,stringValue,multiplier,decimalpoints,offset):

#Parameter
#filePath: 		Pfad und Dateiname in der ein Wert geschrieben wird
#stringValue: 	Wert der nach dem knonvertieren in die Datei geschrieben wird
#multiplier: 	Wert mit dem die Zahl vor der Rundung multipliziert wird
#decimalpoints:	Anzahl Kommastellen 
#offset:        Moeglichkeit um zusaetzliche Berechnungen zub ergaenzen
#Rueckgabe: nichts

    val= myDecode(stringValue)

	# Format anpassen
    if multiplier != 0:
        val = val * multiplier

    #auf 2 Ziffern runden
    if decimalpoints == 0:
        val = int(val)
    elif decimalpoints != 0:
        val = round(val,decimalpoints)

    if offset != 0:
        val = val + offset

    if debug:
        print(filePath + ' ' + str(val))
    else:
        f = open(filePath, 'w')
        f.write(str(val))
        f.close()
    

def mqttVal(topic,stringValue,multiplier,decimalpoints,offset):

#Parameter
#filePath: 		Pfad und Dateiname in der ein Wert geschrieben wird
#stringValue: 	Wert der nach dem knonvertieren in die Datei geschrieben wird
#multiplier: 	Wert mit dem die Zahl vor der Rundung multipliziert wird
#decimalpoints:	Anzahl Kommastellen 
#offset:        Moeglichkeit um zusaetzliche Berechnungen zub ergaenzen
#Rueckgabe: nichts

    val= myDecode(stringValue)

	# Format anpassen
    if multiplier != 0:
        val = val * multiplier

    #auf 2 Ziffern runden
    if decimalpoints == 0:
        val = int(val)
    elif decimalpoints != 0:
        val = round(val,decimalpoints)

    if offset != 0:
        val = val + offset

    if debug:
        print(topic + ' ' + str(val))
    else:
        client.publish(topic, val, qos=1, retain=True)
    

#go-eCharger Parkplatz
response = urllib2.urlopen('http://192.168.178.121/status')
jsondata = json.load(response)
if not (jsondata["nrg"] is None):
    goe_1 = jsondata["nrg"][11]*10
    if debug == True:
        print("Leistung gesamt go-e1: " +str(goe_1))
    goe_1A1 = jsondata["nrg"][5]/10
    goe_1A2 = jsondata["nrg"][6]/10
    goe_1A3 = jsondata["nrg"][4]/10
    if debug == True:
        print("Ampere auf L1 go-e1: " +str(goe_1A1))
        print("Ampere auf L2 go-e1: " +str(goe_1A2))
        print("Ampere auf L3 go-e1: " +str(goe_1A3))
    goe_1L1 = jsondata["nrg"][8]*100
    goe_1L2 = jsondata["nrg"][9]*100
    goe_1L3 = jsondata["nrg"][7]*100
    if debug == True:
        print("Leistung auf L1 go-e1: " +str(goe_1L1))
        print("Leistung auf L2 go-e1: " +str(goe_1L2))
        print("Leistung auf L3 go-e1: " +str(goe_1L3))

#go-eCharger Carport
response = urllib2.urlopen('http://192.168.178.111/status')
jsondata = json.load(response)
if not (jsondata["nrg"] is None):
    goe_2 = jsondata["nrg"][11]*10
    if debug == True:
        print("Leistung gesamt go-e2: " +str(goe_2))
    goe_2A1 = jsondata["nrg"][6]/10
    goe_2A2 = jsondata["nrg"][4]/10
    goe_2A3 = jsondata["nrg"][5]/10
    if debug == True:
        print("Ampere auf L1 go-e2: " +str(goe_2A1))
        print("Ampere auf L2 go-e2: " +str(goe_2A2))
        print("Ampere auf L3 go-e2: " +str(goe_2A3))
    goe_2L1 = jsondata["nrg"][9]*100
    goe_2L2 = jsondata["nrg"][7]*100
    goe_2L3 = jsondata["nrg"][8]*100
    if debug == True:
        print("Leistung auf L1 go-e1: " +str(goe_2L1))
        print("Leistung auf L2 go-e1: " +str(goe_2L2))
        print("Leistung auf L3 go-e1: " +str(goe_2L3))

#EVU Daten
reqdata='{"PM1OBJ1":{"FREQ":"","U_AC":"","I_AC":"","P_AC":"","P_TOTAL":""}}'
response = urllib2.urlopen('http://'+ ipaddress +'/lala.cgi' ,data=reqdata)
jsondata = json.load(response)
#keine Werte gefunden
# echo $evupf1 > /var/www/html/openWB/ramdisk/evupf1
# echo $evupf2 > /var/www/html/openWB/ramdisk/evupf2
# echo $evupf3 > /var/www/html/openWB/ramdisk/evupf3

#SENEC: Gesamtleistung (W) Werte -3000  >> 3000
# if not (jsondata['PM1OBJ1'] ['P_TOTAL'] is None):
#     if writing_in_file:
#         writeVal('/var/www/html/openWB/ramdisk/wattbezug_senec', jsondata['PM1OBJ1'] ['P_TOTAL'],0,0,goe_1 + goe_2)
#     if writing_mqtt:
#         mqttVal('openWB/set/evu/W', jsondata['PM1OBJ1'] ['P_TOTAL'],0,0,goe_1 + goe_2)

#SENEC: Frequenz(Hz) Werte 49.00 >> 50.00
if not (jsondata['PM1OBJ1'] ['FREQ'] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/evuhz',jsondata['PM1OBJ1'] ['FREQ'],0,2,0)
    if writing_mqtt:
        mqttVal('openWB/set/evu/HzFrequenz',jsondata['PM1OBJ1'] ['FREQ'],0,2,0)

#SENEC: Spannung (V) Werte 219.12 >> 223.43
if not (jsondata['PM1OBJ1'] ['U_AC'] [0] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/evuv1', jsondata['PM1OBJ1'] ['U_AC'] [0],0,2,0)
    if writing_mqtt:
        mqttVal('openWB/set/evu/VPhase1', jsondata['PM1OBJ1'] ['U_AC'] [0],0,2,0)
if not (jsondata['PM1OBJ1'] ['U_AC'] [1] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/evuv2', jsondata['PM1OBJ1'] ['U_AC'] [1],0,2,0)
    if writing_mqtt:
        mqttVal('openWB/set/evu/VPhase2', jsondata['PM1OBJ1'] ['U_AC'] [1],0,2,0)
if not (jsondata['PM1OBJ1'] ['U_AC'] [2] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/evuv3', jsondata['PM1OBJ1'] ['U_AC'] [2],0,2,0)
    if writing_mqtt:
        mqttVal('openWB/set/evu/VPhase3', jsondata['PM1OBJ1'] ['U_AC'] [2],0,2,0)

#SENEC: Leistung (W) Werte -2345 >> 3000
# if not (jsondata['PM1OBJ1'] ['P_AC'] [0] is None):
#     writeVal('/var/www/html/openWB/ramdisk/bezugw1', jsondata['PM1OBJ1'] ['P_AC'] [0],0,0,goe_1L1 + goe_2L1)
# if not (jsondata['PM1OBJ1'] ['P_AC'] [1] is None):
#     writeVal('/var/www/html/openWB/ramdisk/bezugw2', jsondata['PM1OBJ1'] ['P_AC'] [1],0,0,goe_1L2 + goe_2L3)
# if not (jsondata['PM1OBJ1'] ['P_AC'] [2] is None):
#     writeVal('/var/www/html/openWB/ramdisk/bezugw3', jsondata['PM1OBJ1'] ['P_AC'] [2],0,0,goe_1L3 + goe_2L3)

#SENEC: Strom (A) Werte 0.88 >> 1.67 
if not (jsondata['PM1OBJ1'] ['I_AC'] [0] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/bezuga1_senec', jsondata['PM1OBJ1'] ['I_AC'] [0],0,2,goe_1A1 + goe_2A1)
    if writing_mqtt:
        mqttVal('openWB/set/evu/APhase1', jsondata['PM1OBJ1'] ['I_AC'] [0],0,2,goe_1A1 + goe_2A1)
if not (jsondata['PM1OBJ1'] ['I_AC'] [1] is None):   
    if writing_in_file: 
        writeVal('/var/www/html/openWB/ramdisk/bezuga2_senec', jsondata['PM1OBJ1'] ['I_AC'] [1],0,2,goe_1A2 + goe_2A2)
    if writing_mqtt:
        mqttVal('openWB/set/evu/APhase2', jsondata['PM1OBJ1'] ['I_AC'] [1],0,2,goe_1A2 + goe_2A2)
if not (jsondata['PM1OBJ1'] ['I_AC'] [2] is None):    
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/bezuga3_senec', jsondata['PM1OBJ1'] ['I_AC'] [2],0,2,goe_1A3 + goe_2A3)
    if writing_mqtt:
        mqttVal('openWB/set/evu/APhase3', jsondata['PM1OBJ1'] ['I_AC'] [2],0,2,goe_1A3 + goe_2A3)

#Batteriedaten:
reqdata='{"ENERGY":{"GUI_BAT_DATA_FUEL_CHARGE":"","GUI_BAT_DATA_POWER":"","GUI_BAT_DATA_VOLTAGE":"","GUI_BAT_DATA_OA_CHARGING":"","GUI_INVERTER_POWER":""}}'
response = urllib2.urlopen('http://'+ ipaddress +'/lala.cgi' ,data=reqdata)
jsondata = json.load(response)

#SENEC: Batterieleistung (W) Werte -345 (Entladen) >> 1200 (laden)
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'] is None):
    writeVal('/var/www/html/openWB/ramdisk/speicherleistung_senec_temp', jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'],0,0,0)
    f = open('/var/www/html/openWB/ramdisk/speicherleistung_senec_temp', 'r')
    value = f.read()
    f.close()
    value = int(value)
    if value > -10 and value < -2:
        if writing_in_file:
            f = open('/var/www/html/openWB/ramdisk/speicherleistung_senec','w')
            f.write("0")
            f.close()
        if writing_mqtt:
            client.publish('openWB/set/houseBattery/W', '0', qos=1, retain=True)
    else:
        if writing_in_file:
            writeVal('/var/www/html/openWB/ramdisk/speicherleistung_senec', jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'],0,0,0)
        if writing_mqtt:
            mqttVal('openWB/set/houseBattery/W', jsondata['ENERGY'] ['GUI_BAT_DATA_POWER'],0,0,0)


#SENEC: Fuellmenge in Prozent Werte 10 >> 55 >> 100
if not (jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/speichersoc_senec', jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'],0,0,0)
    if writing_mqtt:
        mqttVal('openWB/set/houseBattery/%Soc', jsondata['ENERGY'] ['GUI_BAT_DATA_FUEL_CHARGE'],0,0,0)

#SENEC: Leistung Wechselrichter in (W) Werte 
if not (jsondata['ENERGY'] ['GUI_INVERTER_POWER'] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/pvwatt_senec', jsondata['ENERGY'] ['GUI_INVERTER_POWER'],0,0,0)
    if writing_mqtt:
        mqttVal('openWB/set/pv/1/W', jsondata['ENERGY'] ['GUI_INVERTER_POWER'],0,0,0)

#Statistik
reqdata='{"STATISTIC":{"LIVE_BAT_CHARGE":"","LIVE_BAT_DISCHARGE":"","LIVE_GRID_EXPORT":"","LIVE_GRID_IMPORT":"","LIVE_HOUSE_CONS":"","LIVE_PV_GEN":""}}'
response = urllib2.urlopen('http://'+ ipaddress +'/lala.cgi' ,data=reqdata)
jsondata = json.load(response)

#SENEC: Gesamtlademenge (Wh) Werte 1692
if not (jsondata['STATISTIC'] ['LIVE_BAT_CHARGE'] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/speicherikwh_senec', jsondata['STATISTIC'] ['LIVE_BAT_CHARGE'],1000,0,0)
    if writing_mqtt:
        mqttVal('openWB/set/houseBattery/WhImported', jsondata['STATISTIC'] ['LIVE_BAT_CHARGE'],1000,0,0)

#SENEC: Gesamtentlademenge (Wh) Werte 1590
if not (jsondata['STATISTIC'] ['LIVE_BAT_DISCHARGE'] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/speicherekwh_senec', jsondata['STATISTIC'] ['LIVE_BAT_DISCHARGE'],1000,0,0)
    if writing_mqtt:
        mqttVal('openWB/set/houseBattery/WhExported', jsondata['STATISTIC'] ['LIVE_BAT_DISCHARGE'],1000,0,0)

#SENEC: Gesamtimport (Wh) Werte  1809000
# if not (jsondata['STATISTIC'] ['LIVE_GRID_IMPORT'] is None):
#     if writing_in_file:
#         writeVal('/var/www/html/openWB/ramdisk/bezugkwh_senec', jsondata['STATISTIC'] ['LIVE_GRID_IMPORT'],1000,0,0)
#     if writing_mqtt:
#         mqttVal('openWB/set/evu/WhImported', jsondata['STATISTIC'] ['LIVE_GRID_IMPORT'],1000,0,0)
    
# SENEC: Gesamteinspeisung Werte (Wh) 7085000
# if not (jsondata['STATISTIC'] ['LIVE_GRID_EXPORT'] is None):
#     if writing_in_file:
#         writeVal('/var/www/html/openWB/ramdisk/einspeisungkwh_senec', jsondata['STATISTIC'] ['LIVE_GRID_EXPORT'],1000,0,0)
#     if writing_mqtt:
#         mqttVal('openWB/set/evu/WhExported', jsondata['STATISTIC'] ['LIVE_GRID_EXPORT'],1000,0,0)

#SENEC: Gesamt PV Erzeugung (vom WR)  Werte (Wh) 7085000
if not (jsondata['STATISTIC'] ['LIVE_PV_GEN'] is None):
    if writing_in_file:
        writeVal('/var/www/html/openWB/ramdisk/pvewh_senec', jsondata['STATISTIC'] ['LIVE_PV_GEN'],1000,0,0)
    if writing_mqtt:
        mqttVal('openWB/set/pv/1/WhCounter', jsondata['STATISTIC'] ['LIVE_PV_GEN'],1000,0,0)