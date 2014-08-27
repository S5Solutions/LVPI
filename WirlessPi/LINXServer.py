import socket
import sys
from serial import Serial
import binascii
from time import sleep

DEBUG = True


HOST = '10.1.10.48'
PORT = 8889

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'

try:
	s.bind((HOST,PORT))
except (socket.error, KeyboardInterrupt) , msg:
	print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'
s.listen(10)
print 'Socket now listening..'

try: 
	ser = Serial('/dev/ttyAMA0', baudrate = 9600 , timeout=5.0)

	conn, addr = s.accept()
	print 'Connected with ' + addr[0] + ':' + str(addr[1])
except (KeyboardInterrupt), msg:
	print 'Exiting: Keyboard Interrupt'
	sys.exit()

try:
	while 1:
		if(DEBUG): print "step 0: beginning of loop"
		first = conn.recv(1)
		if(DEBUG): print "step 1: LINX recv first"
		if(len(first)):

			hextFirst = hex( ord(first) )
			if(DEBUG): print hextFirst
		
			if hextFirst == '0xff':
				length = conn.recv(1)
				if(DEBUG): print "step 2: LINX recv length"
				hextLength = hex( ord(length) )
				if(DEBUG): print hextLength
				
	
				cmd = conn.recv( ord(length) - 2)
				if(DEBUG): print "step 3: LINX recv cmd"
				hextCmd = binascii.b2a_hex(cmd)
				if(DEBUG): print hextCmd
		
				ser.write(first + length + cmd)
				if(DEBUG): print "step 4: write to arduino"
				
				respFirst = ser.read(1)
				if(DEBUG): print "step 5: ARD read first"
				#if(respFirst)
				if(len(respFirst)) :
					hextRespFirst = hex( ord(respFirst) )		
					if(DEBUG): print hextRespFirst
						
					if hextRespFirst == '0xff':
						if(DEBUG): print "step 6: ARD read length"
						respLength = ser.read()
						hextRespLength = hex( ord(respLength) )
						if(DEBUG): print hextRespLength
					
						if(DEBUG): print "step 7: ARD read cmd"
						respCmd = ser.read( ord(respLength) - 2 )
						hextRespCmd = binascii.b2a_hex(respCmd)
						if(DEBUG): print hextRespCmd
					
						if(DEBUG): print "step 8: send to linx"
						conn.sendall(respFirst + respLength + respCmd)

		if(DEBUG): print "step 9: end of loop"
except (KeyboardInterrupt, TypeError):
	s.close
	conn.close
	print "Exiting: keyboard interrupt"
		









