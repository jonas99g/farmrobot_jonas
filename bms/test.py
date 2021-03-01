import time
import serial
ask_etl = b'\xAA\x09\x04\x22\x00\x23\x00\xF3\x1B'
BMS = serial.Serial(port='/dev/ttyAMA0',baudrate=115200,bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE, timeout=1,xonxoff=0,rtscts=0,dsrdtr=0)

While 1:
    BMS.reset_input_buffer()
    BMS.reset_output_buffer()
    BMS.write(ask_etl)
    BMS.flush()
    BMS.write(ask_etl)
    BMS.flush()
    msg = BMS.read(30)
    print(msg)
    time.sleep(1)