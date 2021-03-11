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



ask_etl = bytes([0xAA, 0x20, 0x7E, 0xC8]) #reg:34,35; [UINT_32] / Resolution 1 s R -->DATA3
ask_packv = bytes([0xAA, 0x14, 0x7E, 0xAF]) #reg:36,37; [FLOAT] / Resolution 1 V R
ask_packc = bytes([0xAA, 0x15, 0xBF, 0x6F]) #reg:38,39; [FLOAT] / Resolution 1 A R
#syspow [FLOAT] / Resolution 1 W R
ask_mincv = bytes([0xAA, 0x17, 0x3F, 0x1E]) #reg:40; [UINT_16] / Resolution 1 mV R
ask_maxcv = bytes([0xAA, 0x16, 0xFE, 0xDE]) #reg:41; [UINT_16] / Resolution 1 mV R
#inbalance of cells (maxcv - mincv 
ask_soc = bytes([0xAA, 0x1A, 0xFE, 0xDB]) #reg:46,47; [UINT_32] / Resolution 0.000001 % R
ask_bmstemp = bytes([0xAA, 0x1B, 0x3F, 0x1B])#reg:48(,42,43); [INT_16] / Resolution 0.1 °C R
ask_bmsstatus = bytes([0xAA, 0x18, 0x7F, 0x1A]) #reg:50 BMS Online Status [UINT_16] / 0x91-Charging, 0x92-Fully Charged, 0x93-Discharging, 0x96-Regenertion, 0x97-Idle, 0x9B-Fault R
ask_nevents = bytes([0xAA, 0x11, 0xBF, 0x1C]) #Read Tiny BMS newest Events


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

def read_etl() {
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
  do_connect()
  etl = read_etl()





"""send ask_sequence twice
receive answer sequence and store it
check init Sequence (eg AA 09 04)
calculate and check CRC16 MODBUS checkbit
read and encode value to variable"""