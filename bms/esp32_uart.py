import sys
import os
import serial
import time
#import paho.mqtt.publish as publish
#import psutil
import string

import machine
machine.freq(240000000)
import esp
#esp.osdebug(None)       # turn off vendor O/S debugging messages
esp.osdebug(0)

def do_connect():
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('Jonas', 'test1234')
        while not wlan.isconnected():
            pass
    print('network config:', wlan.ifconfig())

writeAPIKey = "V13QLD2JANKYVBV1"
mqttAPIKey = "R95SKCL1DYRQNF67"
channelID = "1314526"
mqttHost = "mqtt.thingspeak.com"
mqttUsername = "JonasGessmann"
tTransport = "websockets"
tPort = 80
topic = "channels/" + channelID + "/publish/" + writeAPIKey

#ask_etl = b'\xAA\x09\x04\x22\x00\x23\x00\xF3\x1B'
ask_etl = bytes([0xAA, 0x09, 0x04, 0x22, 0x00, 0x23, 0x00, 0xF3, 0x1B]) #reg:34,35; [UINT_32] / Resolution 1 s R
ask_packv = bytes([0xAA, 0x09, 0x04, 0x24, 0x00, 0x25, 0x00, 0xF0, 0x33]) #reg:36,37; [FLOAT] / Resolution 1 V R
ask_packc = bytes([0xAA, 0x09, 0x04, 0x26, 0x00, 0x27, 0x00, 0xF0, 0xEB]) #reg:38,39; [FLOAT] / Resolution 1 A R
#syspow [FLOAT] / Resolution 1 W R
ask_mincv = bytes([0xAA, 0x09, 0x02, 0x28, 0x00, 0x60, 0x45]) #reg:40; [UINT_16] / Resolution 1 mV R
ask_maxcv = bytes([0xAA, 0x09, 0x02, 0x29, 0x00, 0x81, 0xD4]) #reg:41; [UINT_16] / Resolution 1 mV R
#inbalance of cells (maxcv - mincv 
ask_soc = bytes([0xAA, 0x09, 0x04, 0x2E, 0x00, 0x2F, 0x00, 0xF5, 0x4B]) #reg:46,47; [UINT_32] / Resolution 0.000001 % R
ask_bmstemp = bytes([0xAA, 0x09, 0x02, 0x30, 0x00, 0x8A, 0x44])#reg:48; [INT_16] / Resolution 0.1 °C R
ask_bmsstatus = bytes([0xAA, 0x09, 0x02, 0x32, 0x00, 0x8B, 0x24]) #reg:50 BMS Online Status [UINT_16] / 0x91-Charging, 0x92-Fully Charged, 0x93-Discharging, 0x96-Regenertion, 0x97-Idle, 0x9B-Fault R
ask_nevents = bytes([0xAA, 0x11, 0xBF, 0x1C]) #Read Tiny BMS newest Events
#init_seq_2 = b'\xAA\x09\x04'
#init_seq_4 = b'\xAA\x09\x08'
init_seq_2 = bytes([0xAA,0x09,0x04])
init_seq_4 = bytes([0xAA,0x09,0x08])

int etl = 0 #convert seconds to minutes?
float packv = 0
float packc = 0
float syspow = 0 #SystemPower = PackVoltage * PackCurrent
float mincv = 0 #MinCellV/1000
float maxcv = 0
float cvinbal = 0
int soc = 0 #SOC/1000000
float bmstemp = 0
str bmsstatus = ""
str events = ""

BMS = machine.UART(2, 115200)
BMS.init(baudrate=115200, bits=8, parity=None, stop=1, tx=25, rx=26, timeout=500)

def read_status_2(ask_seq) {
  bms_dump = bytes([])
  BMS.reset_input_buffer()
  BMS.reset_output_buffer()
  BMS.write(ask_seq)
  BMS.flush()
  BMS.write(ask_seq)
  BMS.flush()
  bms_dump = BMS.read()
  msg = BMS.read(size=6)
  return msg
}
def read_status_4(ask_seq) {
  bms_dump = bytes([])
  msg = bytes ([])
  msgc = bytes ([])
  seq = bytes ([])
  seqc = bytes ([])
  pl_len = 8
  total_len = 13
  bms_dump = BMS.read()
  BMS.write(ask_seq)
  BMS.write(ask_seq)
  if (BMS.any() > 0):
    BMS.readinto(msg)
  for (i=0,i<=len(msg),i+=1):
  msgc = [msg[i],msg[i+1],msg[i+2]]
    if msgc == init_seq_4
      j = i
  for (k=0,k<total_len,j+=1):  
    seqc.append(msg[j]) 
  return seq
}
'''
while 1:
  #do_connect()
  etl = int(read_status_4(ask_etl))
  packv = int (read_status_4(ask_packv))

  payload = "etl=" + str(etl) + "&packv=" + str(packv) + "&packc=" + str(packc) + "&syspow=" + str(syspow) + "&mincv=" + str(mincv) + "&soc=" + str(soc) + "&bmstemp=" + str(bmstemp) """+ "&bmsstatus=" + str(bmsstatus""")
  try:
    #publish.single(topic, payload, hostname=mqttHost, transport=tTransport, port=tPort,auth={'username':mqttUsername,'password':mqttAPIKey})
'''





"""send ask_sequence twice
receive answer sequence and store it
check init Sequence (eg AA 09 04)
calculate and check CRC16 MODBUS checkbit
read and encode value to variable"""