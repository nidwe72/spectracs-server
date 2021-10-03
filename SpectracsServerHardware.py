import platform
import cpuinfo
from getmac import get_mac_address as gma

class SpectracsServerServer:

    operatingSystem='operatingSystem'
    cpuArchitecture='cpuArchitecture'
    cpuBrand='cpuBrand'
    mac='mac'
    
    def __init__(self):

        uname = platform.uname()
        #print(cpuinfo.get_cpu_info())
        self.setOperatingSystem(uname.system);
        self.setCpuArchitecture(uname.machine);
        self.setCpuBrand(cpuinfo.get_cpu_info()['brand_raw']);
        self.setMac(gma());

    def setOperatingSystem(self,operatingSystem):
        self.operatingSystem=operatingSystem

    def getOperatingSystem(self):
        return self.operatingSystem

    def setCpuArchitecture(self,cpuArchitecture):
        self.cpuArchitecture=cpuArchitecture

    def getCpuArchitecture(self):
        return self.cpuArchitecture

    def setCpuBrand(self,cpuBrand):
        self.cpuBrand=cpuBrand

    def getCpuBrand(self):
        return self.cpuBrand

    def setMac(self,mac):
        self.mac=mac

    def getMac(self):
        return self.mac




    




