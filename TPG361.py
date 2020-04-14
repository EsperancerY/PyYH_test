# Python ver. 3.8.1
# Ver  : 0.2 
# Date : 2020/04/14 16:50

import serial,socket
import sys,time,datetime


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
		self.initialize()
		self.unit = "Torr"
		
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
	
	def initialize(self):
	
	# 電源 On 後、自動で "COM" コマンドを実行する仕様への対処として、
	#　AYT コマンドを送って COM を止め、ENQ を送って返答を捨ててから get_ID()が通るかを試すメソッドです。
	# もし COM 状態じゃないなら、最初の try が通るのでそのまま True を返します。
	
		try:
			self.get_ID()
		except:
			self.send("\x05")
			self.recv()
			try: self.get_ID()
			except : sys.exit("TPG361_04")
		return True
	
	def get_ID(self):
	
		cmd = "AYT\r\n"
		id = self.query(cmd).rstrip("\r\n")
		return id
		
	def show_network(self):
	
		eth = self.query("ETH\r\n").rstrip("\r\n").split(",")
		mac = self.query("MAC\r\n").rstrip("\r\n")
		if eth[0] == 0 : eth[0] = " Disable "
		elif eth[0] == 1 : eth[0] = " Enable "
		else : sys.exit("TPG361_05")		
		print(" DHCP : %s\n IP Address : %s\n SubnetMask : %s\n	Gateway : %s\n MAC Address : %s\n"%(eth[0],eth[1],eth[2],eth[3],mac) 
		return True	
		
	def get_pressure(self,ch=1):
	
		pr = self.query("PR%d\r\n"%ch).rstrip("\r\n").split(",")		
		return pr
	
	def show_pressure(self,ch=1):
	
		res = self.get_pressure(ch)
		
		if int(res[0]) == 0:
			print("%s [%s]"%res[1],unit)
		elif int(res[0]) == 1:
			print(" ERROR !! Measure result is under-range. ")
		elif int(res[0]) == 2:
			print(" ERROR !! Measure result is over-range. ")
		elif int(res[0]) == 3:
			print(" Sensor ERROR !! Please check up the gurge and TG261.")
		elif int(res[0]) == 4:
			print(" ERROR !! Sensor maybe break down.")
		elif int(res[0]) == 5:
			print(" ERROR !! Cannot find sensor ! Maybe cables are un-plaged.")
		elif int(res[0]) == 6:
			print(" Identification ERROR !! Please check up the equipments.")
			
		return True
	
		
		