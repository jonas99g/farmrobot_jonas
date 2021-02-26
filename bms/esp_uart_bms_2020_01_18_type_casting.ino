HardwareSerial BMS(1); //defining "BMS" as HardwareSerial on UART 1

byte bms_registers_msg[] = {0xAA, 0x09, 0x1A, 0x24, 0x00, 0x25, 0x00, 0x26, 0x00, 0x27, 0x00, 0x28, 0x00, 0x29, 0x00, 0x2E, 0x00, 0x2F, 0x00, 0x30, 0x00, 0x32, 0x00, 0x33, 0x00, 0x34, 0x00, 0x04, 0x01, 0xA8, 0x3F};
byte initSeq[] = {0xAA, 0x09, 0x34};
byte rx_data[52];
float PackVoltage = 0;
float PackCurrent = 0;
float SystemPower = 0;
uint16_t MinCellV = 0; // (1 mV) i+21, i+22 2 bytes
uint32_t SOC = 0; // (0.000001 %)

uint16_t BMSOnline = 0; // maybe dictionary for status output 0x91-Charging, 0x92-Fully Charged, 0x93-Discharging, 0x96-Regenertion, 0x97-Idle, 0x9B-Fault



void setup() {
    BMS.setTimeout(400)
    Serial.begin(115200);
    BMS.begin(115200, SERIAL_8N1, 26, 25); //rx, tx
}


void loop()
{
  askRegisters(); 
}

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
void askRegisters()
{
  byte rx[256] = {};
  int i = 0;
  int j = 0;
  
  BMS.write(bms_registers_msg, 31);
  delay(2);
  BMS.write(bms_registers_msg, 31);

  
  while(BMS.available() > 0) { //read bytes when UART buffer is not empty
    BMS.readBytes(rx, 256); //read bytes to the rx array with the size 156
  }
  //finding start sequence
  for (i = 0; i < 257; i++) {
    byte rxCurrent[] = {rx[i],rx[i+1],rx[i+2]}; 
    if (memcmp(rxCurrent, initSeq, 3) == 0) { //comparing the memory content of the arrays to find the starting sequence of 0xAA, 0x09; 2 bytes long; memcmp returns 0 if it matches
      /* check for buffer overflow Serial.print("found: break at i= ");Serial.println(i);*/ j=i;break;
    }
  }
  

  int PL = (int)rx[j+2];
  Serial.print("PL = ");
  Serial.println(PL);
  for (int n = 0; n <= PL+3); n++) {
    rx_data[n] = rx[j];
    Serial.print(rx_data[n],HEX);
    Serial.print(","); 
    j++;
  }
  Serial.print("\n");
  
  byte PackVoltage_array[4] = {rx_data[5], rx_data[6], rx_data[9], rx_data[10]};
  PackVoltage = bytesToFloat(PackVoltage_array);
  /*
  for (int k = 0; k < 4; k++) {
    Serial.println(PackVoltage_array[k],HEX);
  }*/
  Serial.print("Batterypack Voltage: ");
  Serial.print(PackVoltage);
  Serial.println("V");
  
  byte PackCurrent_array[4] = {rx_data[13], rx_data[14], rx_data[17], rx_data[18]};
  PackCurrent = bytesToFloat(PackCurrent_array);
  /*
  for (int k = 0; k < 4; k++) {
    Serial.println(PackCurrent_array[k],HEX);
  }*/
  Serial.print("Batterypack Current: ");
  Serial.print(PackCurrent);
  Serial.println("A");
  
  SystemPower = PackVoltage * PackCurrent;
  Serial.print("System Power: ");
  Serial.print(SystemPower);
  Serial.println("W");

  byte MinCellV_array[2] = {rx_data[21], rx_data[22]};
  MinCellV = bytesToUint16(MinCellV_array); // (1 mV) i+21, i+22 2 bytes
  /*
  for (int k = 0; k < 2; k++) {
    Serial.println(MinCellV_array[k],HEX);
  }*/
  Serial.print("Minimal Cell Voltage: ");
  Serial.print(MinCellV/1000);
  Serial.println("V");
  
  
  byte SOC_array[4] = {rx_data[25], rx_data[26], rx_data[29], rx_data[30]};
  SOC = bytesToUint32(SOC_array); // Resolution 0.000001 %
  /*
  for (int k = 0; k < 4; k++) {
    Serial.println(SOC_array[k],HEX);
  }*/
  Serial.print("State of Charge: ");
  Serial.print((SOC/1000000));
  Serial.println("%");
}
