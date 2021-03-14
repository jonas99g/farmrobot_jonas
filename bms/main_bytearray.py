import sys
import os
import time
import machine
machine.freq(240000000)
import esp
#esp.osdebug(None)       # turn off vendor O/S debugging messages
esp.osdebug(0)

ask_etl = bytearray([0xAA, 0x20, 0x7E, 0xC8]) #reg:34,35; [UINT_32] / Resolution 1 s R -->DATA3
ask_packv = bytearray([0xAA, 0x14, 0x7E, 0xAF]) #reg:36,37; [FLOAT] / Resolution 1 V R
ask_packc = bytearray([0xAA, 0x15, 0xBF, 0x6F]) #reg:38,39; [FLOAT] / Resolution 1 A R
#syspow [FLOAT] / Resolution 1 W R
ask_mincv = bytearray([0xAA, 0x17, 0x3F, 0x1E]) #reg:40; [UINT_16] / Resolution 1 mV R
ask_maxcv = bytearray([0xAA, 0x16, 0xFE, 0xDE]) #reg:41; [UINT_16] / Resolution 1 mV R
#inbalance of cells (maxcv - mincv 
ask_soc = bytearray([0xAA, 0x1A, 0xFE, 0xDB]) #reg:46,47; [UINT_32] / Resolution 0.000001 % R
ask_bmstemp = bytearray([0xAA, 0x1B, 0x3F, 0x1B])#reg:48(,42,43); [INT_16] / Resolution 0.1 °C R
ask_bmsstatus = bytearray([0xAA, 0x18, 0x7F, 0x1A]) #reg:50 BMS Online Status [UINT_16] / 0x91-Charging, 0x92-Fully Charged, 0x93-Discharging, 0x96-Regenertion, 0x97-Idle, 0x9B-Fault R
ask_nevents = bytearray([0xAA, 0x11, 0xBF, 0x1C]) #Read Tiny BMS newest Events

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
  msg = bytearray([])
  msgc = bytearray([])
  seq = bytearray([])
  seqc = bytearray([])
  etl_init = bytearray([0xAA, 0x20])
  total_len = 16
  BMS.write(ask_etl)
  BMS.write(ask_etl)
  while BMS.any() > 0:
    BMS.readinto(msg)
  for i in msg:
    msgc= msg[i]+msg[i+1]
    if msgc == etl_init:
      j = i
      break
  k=0
  while k<total_len:
    seq += msg[j]
    j+=1
    k+=1
  return seq

print(hex(read_etl()))
#while 1:
  #do_connect()
  #etl = read_etl()
  #print(read_etl())