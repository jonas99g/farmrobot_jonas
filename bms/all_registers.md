Read Tiny BMS online status
Request: 0xAA 0x18 CRC:LSB CRC:MSB
Response: 0xAA 0x18 DATA:LSB DATA:MSB CRC:LSB CRC:MSB /0x91 – Charging, 0x92 – Fully Charged, 0x93 – Discharging, 0x96 – Regeneration, 0x97 – Idle, 0x9B – Fault
Response ERROR: 0xAA 0x00 0x18 ERROR CRC:LSB CRC:MSB

Possible speed sensor for distance and speed calculations
external temperature leads

Not included, but optional in the future:
Cells
Speed
Distance
Distance left
Lifetime Counter
Max Cell Voltage
Ext Temperature
balancing decision bits
(real balancing bits)
number of detected cells
speed

Statistics not included:
total distance
max charge/discharge current
max cell voltage difference
under/over-voltage protection count
charge/discharge over-current protection count
overheat detection count
charging count
full charge count
min/max temperature of pack
statistics last cleared on




34,35 Estimated Time Left [UINT_32] / Resolution 1 s R
36,37 Battery Pack Voltage [FLOAT] / Resolution 1 V R
38,39 Battery Pack Current [FLOAT] / Resolution 1 A R
#syspow [FLOAT] / Resolution 1 W R
40 Minimal Cell Voltage [UINT_16] / Resolution 1 mV R
41 Maximal Cell Voltage [UINT_16] / Resolution 1 mV
inbalance of cells
46,47 State Of Charge [UINT_32] / Resolution 0.000001 % R
48 BMS Internal Temperature [INT_16] / Resolution 0.1 °C R
50 BMS Online Status [UINT_16] / 0x91-Charging, 0x92-Fully Charged, 0x93-Discharging, 0x96-Regenertion, 0x97-Idle, 0x9B-Fault R

51 Balancing Decision Bits [UINT_16] / First Cell - LSB Bit of LSB Byte: 1 - need balancing, 0 - cell no need balance R
52 Real Balancing Bits [UINT_16] / First Cell - LSB Bit of LSB Byte: 1 - balancing, 0 – not balancing R


Settings
301 Fully Discharged Voltage [UINT_16] [1000 to 3500] / Resolution 1 mV R/W
316 Under-Voltage Cutoff [UINT_16] [800 to 3500] / Resolution 1 mV R/W
317 Discharge Over-Current Cutoff [UINT_16] [1 to 750]* / Resolution 1 A R/W
318 Charge Over-Current Cutoff [UINT_16] [1 to 750]* / Resolution 1 A R/W
319 Over-Heat Cutoff [INT_16] [+20 to +90] / Resolution 1 °C R/W
320 Low Temperature Charger Cutoff [INT_16] [-40 to +10] / Resolution 1 °C 

Additional Settings:
fully charged voltage
early balancing threshold
charge finished current
battery capacity
number of series cells
allowed disbalance
pulses per unit (speed sensor?)
distance unit
over-voltage cutoff
manual soc
automatic recovery
precharge pin
precharge duration



Read Tiny BMS newest Events
Request: 0xAA 0x11 CRC:LSB CRC:MSB

Fault messages list
0x02 Under-Voltage Cutoff Occurred
0x03 Over-Voltage Cutoff Occurred
0x04Over-Temperature Cutoff Occurred
0x05 Discharging Over-Current Cutoff Occurred
0x06 Charging Over-Current Cutoff Occurred
0x07 Regeneration Over-Current Cutoff Occurred
0x0A Low Temperature Cutoff Occurred
0x0B Charger Switch Error Detected
0x0C Load Switch Error Detected
0x0D Single Port Switch Error Detected
0x0E External Current Sensor Disconnected (BMS restart required)
0x0F External Current Sensor Connected (BMS restart required)

Warning messages list
Warning ID (0x31 to 0x60) Warning message
0x31 Fully Discharged Cutoff Occurred
0x37 Low Temperature Charging Cutoff Occurred
0x38 Charging Done (Charger voltage too high)
0x39 Charging Done (Charger voltage too low)

Information messages list
Info ID (0x61 to 0x90) Info message
0x61 System Started
0x62 Charging Started
0x63 Charging Done
0x64 Charger Connected
0x65 Charger Disconnected
0x66 Dual Port Operation Mode Activated
0x67 Single Port Operation Mode Activated
0x73 Recovered From Over-Temperature Fault Condition
0x74 Recovered From Low Temperature Warning Condition
0x75 Recovered From Low Temperature Fault Condition
0x76 Recovered From Charging Over-Current Fault Condition
0x77 Recovered From Discharging Over-Current Fault Condition
0x78 Recovered From Regeneration Over-Current Fault Condition
0x79 Recovered From Over-Voltage Fault Condition
0x7A Recovered From Fully Discharged Voltage Warning Condition
0x7B Recovered From Under-Voltage Fault Condition
0x7C External Current Sensor Connected
0x7D External Current Sensor Disconnected
