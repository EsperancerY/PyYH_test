
# Python ver. 3.8.1
# Ver  : 0.2 
# Date : 2020/01/14 20:01

import sys,time,socket

class COM(object):

	def __init__(self,IP,port=1234,GA,GA2=0):
		self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.com.settimeout(1.0)
		self.IP = IP
		self.port = port
		self.GA = GA
		self.GA2 = GA2
		self.open()
		self.gpib_open()
		time.sleep(0.2) # gpib_open 後、コマンド認識不可時間があるため 
		self.set_read_timeout()
		
	def open(self):
		try: self.com.connect((self.IP,self.port))
		except: sys.exit("GPIB_01")
		return True
	
	def close(self):
		try: self.com.close()
		except: sys.exit("GPIB_02")
		return True
	
	def query(self,cmd):
		self.send(cmd)
		time.sleep(0.05)
		recv = self.recv()
		return recv
	
	def send(self,cmd):
		try: self.com.send(cmd.encode("utf-8"))
		except: sys.exit("GPIB_03")
		return True
	
	def recv(self,byte=1024):
		try:
			recv = self.com.recv(byte).decode("utf-8")
		except: sys.exit("GPIB_04")		
		return recv
	
	def gpib_open(self):
		self.send("++mode 1\n")
		self.send("++auto 1\n")
		self.set_GPIB_address(self.GA,self.GA2)
		return True
	
	def check_auto(self):
		au = self.query("++auto\n")
		if au == "1\r\n" : au = "Read_after_Write Mode."
		elif au == "0\r\n" : au = "Non RaW Mode."
		else : sys.exit("GPIB_05")
		return au
		
	def show_auto(self):
		au = self.check_auto()
		if au == "Non RaW Mode": au + " Please use read command."
		print("\n %s\n"%au)
		return True
	
	def set_auto(self,au = 1):
		if au == 1 or au == 0:pass
		else :
			print("\n Invalid Automode value is entered. Please select 0 or 1")
			print(" 1 = Read_after_Write mode, 0 = Non RaW mode.\n")
			sys.exit("GPIB_06")
		self.send("++auto %d"%au)
		if au == 1:
			print("\n Success to set Read_after_Write mode.\n")
		elif au == 0:
			print("\n Success to set Non RaW mode, please use read command.\n")
		return True		
	
	def read(self,byte=1048576):
		self.send("++read eoi\n")
		res = self.recv(byte)
		return res
		
	def show_read(self):
		res = self.read()
		print(res)
		return True		
	
	def set_read_timeout(self,wt = 1000):
		self.send("++read_tmo_ms %d\n"%wt)
		return True
	
	def check_GPIB_address(self):
		ga = self.query("++addr\n")
		try : self.GA = int(ga)
		except :
			data = ga.rstrip("\r\n").split(" ")
			self.GA = int(data[0])
			self.GA2 = int(data[1])
		data = (self.GA,self.GA2)
		return data
	
	def show_GPIB_address(self):
		ga = self.check_GPIB_address()
		print("\n Current 1st GPIB Address = %d,"%ga[0])
		print(" Current 2nd GPIB Address = %d \n"%ga[1])		
		return True
	
	def set_GPIB_address(self,ga,ga2=0):
		if ga2 == 0 : cmd = "++addr %d\n"%ga
		elif 96 <= ga2 <= 126 : cmd = "++addr %d %d\n"%(ga,ga2)
		else:
			print("\n Invalid 2nd GPIB Address is entered. Please Enter 96~126.\n")
			sys.exit("GPIB_07")
		self.send(cmd)
		self.GA = ga
		self.GA2 = ga2
		return True
	
	def check_ID(self):
		id = self.query("*IDN?\n")
		return id
	
	def show_ID(self):
		id = self.check_ID()
		print(id)
		return True
