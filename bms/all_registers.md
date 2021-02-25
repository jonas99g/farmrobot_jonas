Read Tiny BMS online status
Request: 0xAA 0x18 CRC:LSB CRC:MSB
Response: 0xAA 0x18 DATA:LSB DATA:MSB CRC:LSB CRC:MSB /0x91 – Charging, 0x92 – Fully Charged, 0x93 – Discharging, 0x96 – Regeneration, 0x97 – Idle, 0x9B – Fault
Response ERROR: 0xAA 0x00 0x18 ERROR CRC:LSB CRC:MSB


RegNr   Live Data
0 Cell 1 Voltage [UINT_16] / Resolution 0.1 mV R
1 Cell 2 Voltage [UINT_16] / Resolution 0.1 mV R
2 Cell 3 Voltage [UINT_16] / Resolution 0.1 mV R
3 Cell 4 Voltage [UINT_16] / Resolution 0.1 mV R
4 Cell 5 Voltage [UINT_16] / Resolution 0.1 mV R
5 Cell 6 Voltage [UINT_16] / Resolution 0.1 mV R
6 Cell 7 Voltage [UINT_16] / Resolution 0.1 mV R
7 Cell 8 Voltage [UINT_16] / Resolution 0.1 mV R
8 Cell 9 Voltage [UINT_16] / Resolution 0.1 mV R
9 Cell 10 Voltage [UINT_16] / Resolution 0.1 mV R
10 Cell 11 Voltage [UINT_16] / Resolution 0.1 mV R
11 Cell 12 Voltage [UINT_16] / Resolution 0.1 mV R
12 Cell 13 Voltage [UINT_16] / Resolution 0.1 mV R
13 Cell 14 Voltage [UINT_16] / Resolution 0.1 mV R
14 Cell 15 Voltage [UINT_16] / Resolution 0.1 mV R
15 Cell 16 Voltage [UINT_16] / Resolution 0.1 mV R
32,33 BMS Lifetime Counter [UINT_32] / Resolution 1 s R
34,35 Estimated Time Left [UINT_32] / Resolution 1 s R
36,37 Battery Pack Voltage [FLOAT] / Resolution 1 V R
38,39 Battery Pack Current [FLOAT] / Resolution 1 A R
40 Minimal Cell Voltage [UINT_16] / Resolution 1 mV R
41 Maximal Cell Voltage [UINT_16] / Resolution 1 mV R
42 External Temp. Sensor #1 Temperature [INT_16] / Resolution 0.1 °C R
43 External Temp. Sensor #2 Temperature [INT_16] / Resolution 0.1 °C R
44 Distance Left To Empty Battery [UINT_16] / Resolution 1 km R
46,47 State Of Charge [UINT_32] / Resolution 0.000001 % R
48 BMS Internal Temperature [INT_16] / Resolution 0.1 °C R
50 BMS Online Status [UINT_16] / 0x91-Charging, 0x92-Fully Charged, 0x93-Discharging, 0x96-Regenertion, 0x97-Idle, 0x9B-Fault R
51 Balancing Decision Bits [UINT_16] / First Cell - LSB Bit of LSB Byte: 1 - need balancing, 0 - cell no need balance R
52 Real Balancing Bits [UINT_16] / First Cell - LSB Bit of LSB Byte: 1 - balancing, 0 – not balancing R
54 Speed [FLOAT] km/h

Statistics
100,101 Total Distance [UINT_32] / Resolution 0.01 km R
102 Maximal Discharge Current [UINT_16] / Resolution 100 mA R
103 Maximal Charge Current [UINT_16] / Resolution 100 mA R
104 Maximal Cell Voltage Difference [UINT_16] / Resolution 0.1 mV R
105 Under-Voltage Protection Count [UINT_16] / Resolution 1 count R
106 Over-Voltage Protection Count [UINT_16] / Resolution 1 count R
107 Discharge Over-Current Protection Count [UINT_16] / Resolution 1 count R
108 Charge Over-Curent Protection Count [UINT_16] / Resolution 1 count R
109 Over-Heat Protection Count [UINT_16] / Resolution 1 count R
111 Charging Count [UINT_16] / Resolution 1 count R
112 Full Charge Count [UINT_16] / Resolution 1 count R
113 Min. Pack Temperature [INT_8] / Resolution 1 °C Max. Pack Temperature [INT_8] / Resolution 1 °C R
114 Last BMS Reset Event [UINT_8] /0x00-Unknown, 0x01-Low power reset, 0x02-Window watchdog reset, 0x03-Independent watchdog reset, 0x04-Software reset, 0x05-POR/PDR reset, 0x06-PIN reset, 0x07-Options bytes loading reset
    Last Wakeup From BMS Sleep Mode Event [UINT_8] /0x00-Charger connected, 0x01-Ignition,0x02-Discharging detected,0x03-UART communication detected
116 Statistics Last Cleared On Tmestamp [UINT_32] / Resolution 1s R


Settings
301 Fully Discharged Voltage [UINT_16] [1000 to 3500] / Resolution 1 mV R/W
303 Early Balancing Threshold [UINT_16] [1000 to 4500] / Resolution 1 mV R/W
308 Allowed Disbalance [UINT_16] [15 to 100] / Resolution 1 mV R/W
315 Over-Voltage Cutoff [UINT_16] [1200 to 4500] / Resolution 1 mV R/W
316 Under-Voltage Cutoff [UINT_16] [800 to 3500] / Resolution 1 mV R/W
317 Discharge Over-Current Cutoff [UINT_16] [1 to 750]* / Resolution 1 A R/W
318 Charge Over-Current Cutoff [UINT_16] [1 to 750]* / Resolution 1 A R/W
319 Over-Heat Cutoff [INT_16] [+20 to +90] / Resolution 1 °C R/W
320 Low Temperature Charger Cutoff [INT_16] [-40 to +10] / Resolution 1 °C 
332 Automatic Recovery [8 bits LSB] [1 to 30] / Resolution 1 s Reserved R/W
334 Ignition [8 bits LSB] / 0x00-Disabled, 0x01-AID01, 0x02-AIDO2, 0x03-DIDO1, 0x04-DIDO2, 0x05-AIHO1, 0x06-AIHO2
335 Charger Detection [8 bits LSB] /0x01-Internal, 0x02-AIDO1, 0x03-AIDO2, 0x04-DIDO1, 0x05-DIDO2, 0x06-AIHO1, 0x07-AIHO2


Read Tiny BMS newest Events
Request: 0xAA 0x11 CRC:LSB CRC:MSB
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
