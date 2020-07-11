from opcua import Client
from opcua import ua
from random import randint
import time
import datetime
from time import sleep
import socket
url="opc.tcp://127.0.0.1:4840"
host="opc.tcp://127.0.0.1"
port=4840
client = Client(url)
client.connect()
print("Client Connected")

root = client.get_node("ns=2;s=Channel1.Device1.Group1")
result=root.get_children()
count=0
for it in result:
    count+=1
#print(count)
while True:   
    for i in range(count):
        result=root.get_children()
        print(result[i])
        var = result[i].get_value()
        print(var)
        i=i+1
    sleep(1.5)
