from time import sleep
import serial
ser = serial.Serial('COM3', 9600) # Establish the connection on a specific port
counter = 32 # Below 32 everything in ASCII is gibberish
while True:
    # counter +=1
    # numOfBytes = len(str(counter))
    # for x in range(0, len(str(counter))):
        # print(counter)
    # ser.write(b'hello') # Convert the decimal number to ASCII then send it to the Arduino
    ser.write(b'11200\r')
    sleep(5)
    ser.write(b'00200\r')
    sleep(5)
    response = ser.read()
    if (response != None):
        print (response) 
    sleep(.1) # Delay for one tenth of a second
    # if counter == 255:
    #     counter = 32