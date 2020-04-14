
# This is an API of Lakeshore LS218 via USB-GPIB controller Agilent 82357B
# ver. : 1.1
# Date : 2020/04/14

import visa
import sys,time

class LS218(object):
    def __init__(self, gpib_port, gpib_address):
        global rm
        global com
        rm = visa.ResourceManager()
        com = rm.open_resource("GPIB%d::%d" %(gpib_port,gpib_address))
        ID = com.ask("*IDN?\n")
        ID = ID.rstrip("\n\r")
        print "\nModel ID = ", ID
        print "GPIB Port = %d , GPIB Address = %d " %(gpib_port,gpib_address)

    def read(self):
        res = com.read()
        return res
        
    def write(self,cmd):
        com.write(cmd)
        return True        

    def query(self,cmd):
        res = com.query(cmd)        
        return res
    
    def ID(self):
        cmd = "*IDN?\n"
        res = self.query(cmd)
        return res
    
    def measure_all(self):
        cmd  = 'KRDG?0\n'
        res = self.query(cmd)
        return res
        
    def ms(self,ch):
        cmd = 'KRDG?%d\n' %ch
        res = self.query(cmd)
        return res

    def measure12(self):
        ch1 = self.ms(1)
        ch2 = self.ms(2)
        ch12 = ch1,ch2
        return ch12
        
    def measure123(self):
        ch0 = self.measure_all()
        ch0 = ch0.split(",")
        ch1 = ch0[0]
        ch2 = ch0[1]
        ch3 = ch0[2]
        ch13 = ch1,ch2,ch3
        return ch13
        
    def reset(self):
        cmd = "*RST\n"
        st = time.time()
        try:
            self.write(cmd)
            print "Now Reseting LS218, please wait about 10 sec..."
            time.sleep(5)
        except:
            print "Fail to send reset command. Please check RS connection etc..."
            sys.exit(1)

        J = False
        while J == False:
            time.sleep(1)
            try:
                self.ID()
                J = True
                ft = time.time()
                pt = ft-ct
            except: pass
        print "Finish. Reset time = %.3f " %pt
        
    def set_curve(self,ch,curve):
    
        if curve == "NONE": curve = 0
        elif curve == "DT-470": curve = 1
        elif curve == "DT-500": curve = 2
        elif curve == "CTI-Diode": curve = 3
        elif curve == "DT-670": curve = 4
        else:pass
            
        cmd = "INCRV%d,%d\n"%(ch,curve)
        cmd2 = "INCRV?%d\n"%ch
        self.write(cmd)
        res = self.query(cmd2)
        
        if int(res) == curve:
            if curve == 0: sc = "NONE"
            elif curve == 1: sc = "DT-470"
            elif curve == 2: sc = "DT-500"
            elif curve == 3: sc = "CTI-Diode"
            elif curve == 4 : sc = "DT-670"
            else : sc = "User-Setting Curve"
            print "Complete to set Input Curve Parameter, Chanel = %d, Curve = %s. " %(ch,sc)
        else:
            print "Maybe, fail to set Input Curve. Please check the following responce, and so on..."
            print res
    
    def check_curve(self):
        n=1
        cl = []
        while n <= 8:
            cmd = "INCRV?%d\n"%n
            res = self.query(cmd)
            cl.append(int(res))
            n += 1
        
        n =1
        while n <=8:
            if cl[n-1] == 0: sc = "NONE"
            elif cl[n-1] == 1: sc = "DT-470"
            elif cl[n-1] == 2: sc = "DT-500"
            elif cl[n-1] == 3: sc = "CTI-Diode"
            elif cl[n-1] == 4 : sc = "DT-670"
            else : cl[n-1] = "User-Setting Curve"
            print " Channel %d = %s. " %(n,sc)
            n +=1
    
    def timer(self,st,wt):
        
        Judge = False
        while Judge == False:
            ct = time.time()
            if ct >= st + wt:
                Judge = True
            else : pass
            
        return True
        
        
        
    