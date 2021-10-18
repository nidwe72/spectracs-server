import platform
import cpuinfo
from getmac import get_mac_address as gma
import SpectralSensorName

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

class SpectralSensor:

    name="spectralSensor"

    def __init__(self):
        self.setName("spectralSensor")

    def __setName(self,name):
        self.name=name;

    def getName(self):
        return self.name

class AmsSpectralSensor(SpectralSensor):

    gain=3
    
    def __init__(self):
        Base.__init__(self)

    def setGain(self,gain):
        self.gain=gain;

    def getGain(self):
        return self.gain


class AmsAs7262SpectralSensor(AmsSpectralSensor):

    def __init__(self):

        Base.__init__(self)

        self.setName(SpectralSensorName.SpectralSensorName.AMS_7262)








    




