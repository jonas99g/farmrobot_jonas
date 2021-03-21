import numpy as np
import wiotp.sdk.device
from time import sleep
from datetime import datetime
import pymodbus.client.sync

dev_port = '/dev/ttyUSB0'
modbus_client = pymodbus.client.sync.ModbusSerialClient(method='rtu', port=dev_port, baudrate=115200, parity='N',
                                                        bytesize=8, stopbits=1, timeout=2, strict=False)
my_config = wiotp.sdk.device.parseConfigFile("device.yaml")
mqtt_client = wiotp.sdk.device.DeviceClient(config=my_config, logHandlers=None)


def connect_modbus():
    if not modbus_client.is_socket_open():
        modbus_client.connect()
    print("connect_modbus: ok")


def connect_mqtt():
    mqtt_client.connect()
    print("connect_mqtt: ok")


def convert(array, da_type):
    return np.array(array, dtype=np.uint16).view(dtype=da_type)[0]


def read_registers(address, count):
    while True:
        result = modbus_client.read_holding_registers(address, count, unit=0xAA)
        if not result.isError():
            register = result.registers
            return register


def ask_registers():
    read_registers(0, 1)
    lifetime_counter = (convert(read_registers(32, 2), np.uint32))/60  # min
    time_left = (convert(read_registers(34, 2), np.uint32))/60  # min
    pack_voltage = convert(read_registers(36, 2), np.float32)  # V
    pack_current = convert(read_registers(38, 2), np.float32)  # C
    min_cell = (read_registers(40, 1)[0])/1000  # V
    max_cell = (read_registers(41, 1)[0])/1000  # V
    cell_diff = (read_registers(104, 1)[0])/10000  # V
    soc = (convert(read_registers(46, 2), np.uint32))/1000000  # %
    bms_temperature = (read_registers(48, 1)[0])/10  # °C
    bms_online = hex(read_registers(50, 1)[0])
    max_discharge_current = (read_registers(102, 1)[0])/1000  # A
    max_charge_current = (read_registers(103, 1)[0])/1000  # A
    charge_count = read_registers(111, 1)[0]

    f_data = {
        'datetime': str(now),
        'lifetime_counter': "%.2f" % lifetime_counter,
        'time_left': "%.2f" % time_left,
        'pack_voltage': "%.2f" % pack_voltage,
        'pack_current': "%.2f" % pack_current,
        'min_cell': "%.2f" % min_cell,
        'max_cell': "%.2f" % max_cell,
        'cell_diff': "%.2f" % cell_diff,
        'soc': "%.2f" % soc,
        'bms_temperature': "%.1f" % bms_temperature,
        'bms_online': str(bms_online),
        'max_discharge_current': "%.2f" % max_discharge_current,
        'max_charge_current': "%.2f" % max_charge_current,
        'charge_count': str(charge_count)
        }
    print(f_data)
    print("stored register values: ok")
    return f_data


def publish(p_data):
    mqtt_client.publishEvent(eventId="status", msgFormat="json", data=p_data, qos=0, onPublish=print("publish: ok"))


def output_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    # current_datetime = now.strftime("%Y-%M-%D-%H-%M")
    print(now)
    print("-------------------------------------------------------------------")
    print(current_time)
    print("-------------------------------------------------------------------")
    return(now)


while True:
    now = output_time()
    connect_modbus()
    connect_mqtt()
    my_data = ask_registers()
    publish(my_data)
    sleep(10)
