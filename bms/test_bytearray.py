ask_etl = bytearray([0xAA, 0x20, 0x7E, 0xC8]) 

def read_etl():
    msg = ask_etl[1:2]
    return msg
a = read_etl()
for i in a:
    print(hex(i))