import numpy as np
import wiotp.sdk.device
import pymodbus.client.sync

# Modbus client
dev_port = '/dev/ttyUSB0'
modbus_client = pymodbus.client.sync.ModbusSerialClient(method='rtu', port=dev_port, timeout=2, baudrate=115200)
modbus_client.connect()

myConfig = wiotp.sdk.device.parseConfigFile("device.yaml")
mqtt_client = wiotp.sdk.device.DeviceClient(config=myConfig, logHandlers=None)
mqtt_client.connect()


def convert(array, da_type):
    return np.array(array, dtype=np.uint16).view(dtype=da_type)[0]


def read_registers(address, count):
    return modbus_client.read_holding_registers(address, count, unit=0xAA).registers


modbus_client.read_holding_registers(0, 1, unit=0xAA)

lifetime_counter = convert(read_registers(32, 2), np.uint32)
time_left = convert(read_registers(34, 2), np.uint32)
pack_voltage = convert(read_registers(36, 2), np.float32)
pack_current = convert(read_registers(38, 2), np.float32)
min_cell = read_registers(40, 1)[0]
max_cell = read_registers(41, 1)[0]
cell_diff = read_registers(104, 1)[0]
soc = convert(read_registers(46, 2), np.uint32)
bms_temperature = read_registers(48, 1)[0]
bms_online = read_registers(50, 1)[0]
max_discharge_current = read_registers(102, 1)[0]
max_charge_current = read_registers(103, 1)[0]
charge_count = read_registers(111, 1)[0]

myData={'name' : 'foo', 'cpu' : 60, 'mem' : 50}
mqtt_client.publishEvent(eventId="status", msgFormat="json", data=myData, qos=0, onPublish=None)
mqtt_client.disconnect()