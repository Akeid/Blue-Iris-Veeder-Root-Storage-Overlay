import serial
import time
import datetime
import os


from time import sleep
from collections import deque




PORT_COM = "COM6"
THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))

ser = serial.Serial(
    port=PORT_COM,\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)


codes= "\x01I20100" #SOH20100, SOH is ctrl+A, I201 is tanks, 00 is all tanks

def writeClipBoard(lineData = "", wipe=False):
    try:
        if wipe:
            with open(THIS_FOLDER + "\\" + "veederroot" + ".txt", "w") as p:
                p.close()
        else:
            with open(THIS_FOLDER + "\\" + "veederroot" + ".txt", "a+") as f:
                f.write(lineData)
                f.close()
    except PermissionError:
        print("Permission error occured in the writeClipBoard() function, trying again...")
        sleep(1)


def readData():
    buffer = ""
    ser.write(codes.encode())
    while True:
        oneByte = ser.read(1)
        if oneByte == b'\x03':    #method should returns bytes
            print(buffer)
            #storeBuffer(buffer)
            #print("now printing the byte value")
            byte_buffer = bytes(buffer, 'utf-8')
            #print(byte_buffer)
            #print("now printing the actual byte values")
            #for byte in bytes(buffer, 'utf-8'):
                #print(byte, end=' ')
            #print("printing the 2-3 value")

            ###############
            regWestGal = byte_buffer[214:218].decode()
            regEastGal = byte_buffer[293:297].decode()
            premGal = byte_buffer[451:455].decode()
            dieselGal = byte_buffer[372:376].decode()

            totalRegularGal = int(regWestGal) + int(regEastGal)

            totalRegular = "Total Reg: " + str(totalRegularGal)



            regWest = "Reg West:  " + byte_buffer[214:218].decode()
            regEast = "Reg East:  " + byte_buffer[293:297].decode()
            prem = "Premium:   " + byte_buffer[451:455].decode()
            diesel = "Diesel:    " + byte_buffer[372:376].decode() + '\n'
            timestamp = "Last Updated: \n" + datetime.datetime.now().strftime("%m-%d-%y at \n%I:%M %p")

            print(totalRegular)
            print(regWest)
            print(regEast)
            print(prem)
            print(diesel)
            print(timestamp)

            writeClipBoard(0, wipe=True)
            sleep(0.1)
            writeClipBoard(totalRegular + '\n')
            sleep(0.1)
            writeClipBoard(prem + '\n')
            sleep(0.1)
            writeClipBoard(diesel + '\n' + '\n')
            sleep(0.1)
            writeClipBoard(timestamp)
            
            
            
            break
        else:
            buffer += oneByte.decode()

while True:
    print("Polling the veeder root now....")
    readData()
    time.sleep(600) # Refreshed every 10 min
    
