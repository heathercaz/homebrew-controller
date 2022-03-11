# Importing Libraries
import serial
import time

letter = 'j'
ser = serial.Serial('COM3', 9600) #Connect to Com3, baud = 9600
time.sleep(2) # Need this or race condition will happen!!

# ser.write('q'.encode()) # turn on red light
ser.write('h'.encode()) # turn on yellow light