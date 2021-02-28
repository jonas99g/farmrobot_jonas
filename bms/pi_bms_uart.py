
import serial
import time

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
init_seq_2 = bytes([0xAA, 0x09, 0x04])
init_seq_4 = bytes([0xAA, 0x09, 0x08])

int etl #convert seconds to minutes?
float packv 
float packc 
float syspow
float mincv
float maxcv
float cvinbal
int soc
float bmstemp
str bmsstatus
str events
#initialize serial
#esp: void setup() BMS.begin(115200, SERIAL_8N1, 26, 25); //rx, tx
BMS = serial.Serial(port='/dev/ttyAMA0',baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, timeout=1,xonxoff=0,rtscts=0,dsrdtr=0,write_timeout=1,)

def read_status(ask_seq,init_seq,output_variable,pl_len) {
  bms_dump = bytes([])
  msg = bytes ([])
  BMS.reset_input_buffer()
  BMS.reset_output_buffer()
  BMS.write(ask_seq)
  BMS.flush()
  BMS.write(ask_seq)
  BMS.flush()
  bms_dump = BMS.read_until(init_seq)
  msg = BMS.read((pl_len+5))
  
  return output_variable
}


#send ask_sequence twice
#receive answer sequence and store it
#check init Sequence (eg AA 09 04)
#calculate and check CRC16 MODBUS checkbit
#read and encode value to variable




#ESP Code

#write ask_sequence
#read UART buffer and storing in cache
#finding start sequence by comparing
#reading payload length and reading through length + checkbit
#print all received data
  byte PackVoltage_array[4] = {rx[j+5], rx[j+6], rx[j+9], rx[j+10]};
  PackVoltage = bytesToFloat(PackVoltage_array);
  
  byte PackCurrent_array[4] = {rx[j+13], rx[j+14], rx[j+17], rx[j+18]};
  PackCurrent = bytesToFloat(PackCurrent_array);
  
  SystemPower = PackVoltage * PackCurrent;

  byte MinCellV_array[2] = {rx[j+21], rx[j+22]};
  MinCellV = bytesToUint16(MinCellV_array); // (1 mV) i+21, i+22 2 bytes
  MinCellV/1000)
  
  byte SOC_array[4] = {rx[j+29], rx[j+30], rx[j+33], rx[j+34]};
  SOC = bytesToUint32(SOC_array); // Resolution 0.000001 %
  (SOC/1000000)
}
  

  
  
#encoding madness of C++
float bytesToFloat(byte byte_array[4])
{
  float float_var;
  memcpy(&float_var,byte_array,4);
  return float_var;
}
uint16_t bytesToUint16(byte byte_array[2])
{
  uint16_t int_var;
  memcpy(&int_var,byte_array,2);
  return int_var;
}
uint32_t bytesToUint32(byte byte_array[4])
{
  uint32_t int_var;
  memcpy(&int_var,byte_array,4);
  return int_var;
}



