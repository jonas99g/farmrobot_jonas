import sys
import os
import serial
import time
import paho.mqtt.publish as publish
import psutil
import string


writeAPIKey = "V13QLD2JANKYVBV1"
mqttAPIKey = "R95SKCL1DYRQNF67"
channelID = "1314526"
mqttHost = "mqtt.thingspeak.com"
mqttUsername = "JonasGessmann"
tTransport = "websockets"
tPort = 80
topic = "channels/" + channelID + "/publish/" + writeAPIKey

ask_etl = b'\xAA\x09\x04\x22\x00\x23\x00\xF3\x1B'#ask_etl = bytes([0xAA, 0x09, 0x04, 0x22, 0x00, 0x23, 0x00, 0xF3, 0x1B]) #reg:34,35; [UINT_32] / Resolution 1 s R
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
init_seq_2 = b'\xAA\x09\x04'
init_seq_4 = b'\xAA\x09\x08'

int etl #convert seconds to minutes?
float packv 
float packc 
float syspow #SystemPower = PackVoltage * PackCurrent
float mincv #MinCellV/1000
#float maxcv
#float cvinbal
int soc #SOC/1000000
float bmstemp
#str bmsstatus
#str events
BMS = serial.Serial(port='/dev/ttyAMA0',baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, timeout=1,xonxoff=0,rtscts=0,dsrdtr=0,write_timeout=1,)

while 1:
  etl = int(read_status_4(ask_etl))

  payload = "etl=" + str(etl) + "&packv=" + str(packv) + "&packc=" + str(packc) + "&syspow=" + str(syspow) + "&mincv=" + str(mincv) + "&soc=" + str(soc) + "&bmstemp=" + str(bmstemp) """+ "&bmsstatus=" + str(bmsstatus""")
  try:
    publish.single(topic, payload, hostname=mqttHost, transport=tTransport, port=tPort,auth={'username':mqttUsername,'password':mqttAPIKey})


def read_status_2(ask_seq) {
  bms_dump = bytes([])
  BMS.reset_input_buffer()
  BMS.reset_output_buffer()
  BMS.write(ask_seq)
  BMS.flush()
  BMS.write(ask_seq)
  BMS.flush()
  bms_dump = BMS.read_until(init_seq_2)
  msg = BMS.read(size=6)
  return msg
}
def read_status_4(ask_seq) {
  bms_dump = bytes([])
  msg = bytes ([])
  pl_len = 8
  BMS.reset_input_buffer()
  BMS.reset_output_buffer()
  BMS.write(ask_seq)
  BMS.flush()
  BMS.write(ask_seq)
  BMS.flush()
  bms_dump = BMS.read_until(init_seq_4)
  msg = BMS.read(size=(pl_len+5))
  return msg
}



"""send ask_sequence twice
receive answer sequence and store it
check init Sequence (eg AA 09 04)
calculate and check CRC16 MODBUS checkbit
read and encode value to variable"""