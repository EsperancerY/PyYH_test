
# Python ver. 3.8.1
# Ver  : 0.2 
# Date : 2020/04/26 16:21

import sys,time,socket,struct

class NW(object):

    def __init__(self,IP="157.16.88.72",port=62500,pw = b"ogawahideo\x0d"):
        self.com = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.com.settimeout(1.0)
        self.IP = IP
        self.port = port
        try : pw = pw.encode()
        except : pass
        self.login(pw)        
        
    def login(self,pw):
        try: self.com.connect((self.IP,self.port))
        except: sys.exit("702NW_01")
        res = self.recv()
        if res == b"login" : 
            res = self.query(pw)
            if res == b"OK" : pass
            else : sys.exit("702NW_02")
        else : sys.exit("702NW_03")
        return True

    def query(self,cmd,wt = 0.05):
        self.send(cmd)
        time.sleep(wt)
        recv = self.recv()
        return recv
    
    def send(self,cmd):
        try: self.com.send(cmd)
        except: sys.exit("702NW_04")
        return True
# チェックサムが 0x00-0xFF までの値をとり得る一方、UTF-8 は 7F までのため、
# encode() はこのメソッド内にはつけないでください。
        
    def recv(self,byte=1024):
        try: recv = self.com.recv(byte)
        except: sys.exit("702NW_05")        
        return recv
# チェックサムが 0x00-0xFF までの値をとり得る一方、UTF-8 は 7F までのため、
# decode() はこのメソッド内にはつけないでください。
        
    def makecmd(self,cmd):
        cmd0 = cmd
        try:cmd = cmd.decode()
        except:pass
        cmd = cmd.split(":")
        if len(cmd) != 1 :
            i = 1
            cmd2 = cmd[0].encode()+b":"
            while i < len(cmd) :
                parameter = cmd[i].split("=")
                cmd[i] = parameter[0].encode()+b"="+struct.pack("<H",len(parameter[1].encode()))+parameter[1].encode()
                cmd2 = cmd2 + cmd[i]
                i += 1
            cmd = cmd2
        else: 
            try : cmd = cmd0.encode()+ b":"
            except : cmd = cmd + b":"
        size = struct.pack("<H",len(cmd))
        checksum = struct.pack("<H",sum(cmd))
        cmd = b"T2" + size + cmd + checksum        
        return cmd    
        
# 引数 cmd の中身は、コマンド文、パラメータ指定文をすべてセパレータ":"で分けることとする。
# たとえば "ECRNT:MODE=0:RAGNE=0" のようにする。
# パラメータがないときは、コマンド文だけにする。たとえば "ECRNT".
