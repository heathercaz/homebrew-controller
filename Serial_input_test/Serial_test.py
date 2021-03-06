# Importing Libraries
import serial
import time

# letter = 'j'
ser = serial.Serial('COM3', 9600, parity = serial.PARITY_EVEN) #Connect to Com3, baud = 9600
time.sleep(2) # Need this or race condition will happen!!

ser.write('!'.encode())
ser.write(bytes([4]))

ser.write('#'.encode()) 
ser.write(bytes([1])) # Step
ser.write(bytes([70])) # time
ser.write('m'.encode()) # unit
ser.write(bytes([30])) # temp
ser.write(bytes([1])) # stage
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([2])) # turn on yellow light
ser.write(bytes([34]))
ser.write('m'.encode())
ser.write(bytes([65]))
ser.write(bytes([3]))
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([3])) # turn on yellow light
ser.write(bytes([66]))
ser.write('h'.encode())
ser.write(bytes([23]))
ser.write(bytes([6]))
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([4])) # turn on yellow light
ser.write(bytes([0]))
ser.write('h'.encode())
ser.write(bytes([88]))
ser.write(bytes([5]))
ser.write('&'.encode())

ser.write('#'.encode()) 
ser.write(bytes([5])) # Step
ser.write(bytes([70])) # time
ser.write('m'.encode()) # unit
ser.write(bytes([30])) # temp
ser.write(bytes([1])) # stage
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([6])) # turn on yellow light
ser.write(bytes([34]))
ser.write('m'.encode())
ser.write(bytes([65]))
ser.write(bytes([3]))
ser.write('&'.encode())

time.sleep(2)

ser.write('#'.encode()) # turn on red light
ser.write(bytes([7])) # turn on yellow light
ser.write(bytes([66]))
ser.write('h'.encode())
ser.write(bytes([23]))
ser.write(bytes([6]))
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([8])) # turn on yellow light
ser.write(bytes([0]))
ser.write('h'.encode())
ser.write(bytes([88]))
ser.write(bytes([5]))
ser.write('&'.encode())

ser.write('#'.encode()) 
ser.write(bytes([9])) # Step
ser.write(bytes([70])) # time
ser.write('m'.encode()) # unit
ser.write(bytes([30])) # temp
ser.write(bytes([1])) # stage
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([1])) # turn on yellow light
ser.write(bytes([34]))
ser.write('m'.encode())
ser.write(bytes([65]))
ser.write(bytes([3]))
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([2])) # turn on yellow light
ser.write(bytes([66]))
ser.write('h'.encode())
ser.write(bytes([23]))
ser.write(bytes([6]))
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([3])) # turn on yellow light
ser.write(bytes([0]))
ser.write('h'.encode())
ser.write(bytes([88]))
ser.write(bytes([5]))
ser.write('&'.encode())

ser.write('#'.encode()) 
ser.write(bytes([13])) # Step
ser.write(bytes([70])) # time
ser.write('m'.encode()) # unit
ser.write(bytes([30])) # temp
ser.write(bytes([1])) # stage
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([14])) # turn on yellow light
ser.write(bytes([34]))
ser.write('m'.encode())
ser.write(bytes([65]))
ser.write(bytes([3]))
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([15])) # turn on yellow light
ser.write(bytes([66]))
ser.write('h'.encode())
ser.write(bytes([23]))
ser.write(bytes([6]))
ser.write('&'.encode())

ser.write('#'.encode()) # turn on red light
ser.write(bytes([16])) # turn on yellow light
ser.write(bytes([0]))
ser.write('h'.encode())
ser.write(bytes([88]))
ser.write(bytes([5]))
ser.write('&'.encode())

print("done")
# print('q'.encode())