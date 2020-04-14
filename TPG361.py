import serial,socket
import sys,time,datetime

#'0,192.168.100.83,255.255.255.0,192.168.100.1\r\n\'

class TPG361(object):

	def __init__(self,adp="Ethernet",IP = "192.168.11.162",port = 8000):
	
		self.adp = adp
		if adp == "Ethernet" :
			self.IP = IP
			self.port = port
			self.connect()
		else :
			self.sp = com
			self.ser_connect()
		
	def connect(self):
		self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.com.settimeout(1.0)
		try: self.com.connect((self.IP,self.port))
		except: sys.exit("TPG361_01")
		return True

	def ser_connect(self,baudrate=9600):
		try: self.com = serial.Serial(
				port = self.sp,
				baudrate = baudrate,
				bytesize=8,
				parity=serial.PARITY_NONE,
				stopbits=1,				
				timeout=0.2,
				writeTimeout=0.2)
		except: sys.exit("TPG361_02")
		return True
	
	def ser_close(self):
		self.com.close()
		return True

	def recv(self,byte = 1024):
		if self.adp == "Ethernet":
			res = self.com.recv(byte).decode()
		else : self.com.read(byte).decode()
		return res		

	def send(self,cmd):
		if self.adp == "Ethernet":
			self.com.send(cmd.encode())
		else : self.com.write(cmd.encode())
		return True

	def query(self,cmd,byte=1024):
		self.send(cmd)
		res = self.recv()
		if res == "\x06\r\n" : self.send("\x05")
		else : sys.exit("TPG361_03")
		res = self.recv()
		return res