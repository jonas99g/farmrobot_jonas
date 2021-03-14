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

ask_etl = bytearray(b'\xAA\x20\x7E\xC8') #reg:34,35; [UINT_32] / Resolution 1 s R -->DATA3
ask_packv = bytearray(b'\xAA\x14\x7E\xAF') #reg:36,37; [FLOAT] / Resolution 1 V R
ask_packc = bytearray(b'\xAA\x15\xBF\x6F') #reg:38,39; [FLOAT] / Resolution 1 A R
#syspow [FLOAT] / Resolution 1 W R
ask_mincv = bytearray(b'\xAA\x17\x3F\x1E') #reg:40; [UINT_16] / Resolution 1 mV R
ask_maxcv = bytearray(b'\xAA\x16\xFE\xDE') #reg:41; [UINT_16] / Resolution 1 mV R
#inbalance of cells (maxcv - mincv 
ask_soc = bytearray(b'\xAA\x1A\xFE\xDB') #reg:46,47; [UINT_32] / Resolution 0.000001 % R
ask_bmstemp = bytearray(b'\xAA\x1B\x3F\x1B') #reg:48(,42,43); [INT_16] / Resolution 0.1 °C R
ask_bmsstatus = bytearray(b'\xAA\x18\x7F\x1A') #reg:50 BMS Online Status [UINT_16] / 0x91-Charging, 0x92-Fully Charged, 0x93-Discharging, 0x96-Regenertion, 0x97-Idle, 0x9B-Fault R
ask_nevents = bytearray(b'\xAA\x11\xBF\x1C') #Read Tiny BMS newest Events

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

BMS = machine.UART(2, 115200)
BMS.init(baudrate=115200, bits=8, parity=None, stop=1, tx=25, rx=26, timeout=500)

def read_etl():
  bms_dump = bytearray(b'')
  msg = bytearray(b'')
  msgc = bytearray(b'')
  seq = bytearray(b'')
  seqc = bytearray(b'')
  etl_init = bytearray(b'\xAA\x20')
  total_len = 16
  BMS.readinto(bms_dump)
  BMS.write(ask_etl)
  BMS.write(ask_etl)
  while BMS.any() > 0:
    BMS.readinto(msg)
  for i in msg & msgc != etl_init:
    msgc= msg[i]+msg[i+1]
    j = i
  k=0
  while k<total_len:
    seq.append(msg[j])
    j+=1
    k+=1
  return seq

print(read_etl())
#while 1:
  #do_connect()
  #etl = read_etl()
  #print(read_etl())