#!/usr/bin/python
import serial,time,sys
from binascii import unhexlify
import time
import argparse
import os

def ByteToHex( byteStr ):
	return ''.join( [ "%02X " % ord( x ) for x in str(byteStr) ] ).strip()

def getchecksum( packet ):
	checksum = 255
	for el in unhexlify(packet):
		checksum ^= ord(el)
	return checksum
	
def getlength( packet ):
	longueur = len(packet)/2+1
	return hex(longueur).split('x')[-1].zfill(2)

def tosend(string):
	withtype = '00'+string
	lenght = getlength(withtype)
	print ('lenght is ' + lenght)
	checksum = getchecksum(lenght+withtype)
	print ('cheksum is ' + hex(checksum))
	finaltosend = '01'+lenght+withtype+hex(checksum)[2:].zfill(2)
	print ('sending ' + finaltosend)
	ser.write(unhexlify(finaltosend))
	
def sendack():
	ser.write(unhexlify('06'))

def toanalyse(type,needed='',data=''):
	count = 0
	while 1:
		begin = ser.read()
		beginstr = str(ByteToHex(begin))
		if beginstr in ['15','01','18','06']:
			print('received ' + beginstr)
			if beginstr == '01':
				length = ser.read()
				lengthstr = str(ByteToHex(length))
				print('data frame lenght is ' +lengthstr)
				data = ser.read(int(lengthstr,16))
				datastr= str(ByteToHex(data))
				print ('full frame is ' + beginstr+ ' ' +lengthstr + ' '+datastr)
				if type=='data':
					if needed != '':
						if datastr[0:5] == needed:
							print('received wanted frame')
							sendack()
							return datastr[6:-3]
				sendack()
			elif beginstr == '06':
				if type=='ack':
					print('received waiting ack ')
					return
			else:
				sendack()
				tosend(data)
				toanalyse(type,needed,data)
		time.sleep(0.1)
def toread():
	while 1:
		begin = ser.read()
		beginstr = str(ByteToHex(begin))
		print('received ' + beginstr)

parser = argparse.ArgumentParser(description='Zwave Network backup Script Jeedom')
parser.add_argument("--name", help="Name", type=str)
parser.add_argument("--port", help="Port for OZW", type=str)
args = parser.parse_args()

ser = serial.Serial(
	port=args.port,
	baudrate=115200,
	bytesize=serial.EIGHTBITS,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE
)
bin =''
x=0
while x <131072:
	print('XXXXXXXXXX is ' + str(x))
	begin=hex(x).split('x')[-1].zfill(6)
	print('want to send '+'2a' + begin +'0040')
	tosend('2a' + begin +'0040')
	toanalyse('ack','','2a' + begin +'0040')
	result=toanalyse('data','01 2A','2a' + begin +'0040')
	bin=bin+result
	x = x+64
st=time.time()
file = "backupnetwork-"+str(st)+"-"+args.name+".bin"
directory = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'data')
file = open(os.path.join(directory,file),"w") 
file.write(bin.replace(' ',''))
file.close()
ser.close()