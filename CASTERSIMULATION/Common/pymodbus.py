from pyModbusTCP.client import ModbusClient

client = ModbusClient(host="10.17.13.32",port=502,auto_open=True)
reg = client.read_coils(3,0)

print("register value is :", reg)
