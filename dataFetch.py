import subprocess, csv, time
from datetime import datetime

class UbuntuCPUData:
    def __init__(self):
        self.__CPUrawData = subprocess.run(["top", "-b", "-n", "1"], stdout=subprocess.PIPE, shell=False, text=True) #get raw Ubuntu top CPU data
        self.__CPUrawGrep = subprocess.run(["grep", "%Cpu(s)"], input=self.__CPUrawData.stdout, shell=False, capture_output=True, text=True) #data gets piped into the grep command
        #output: %Cpu(s):  1.1 us,  0.0 sy,  0.0 ni, 98.9 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
        self.__timeAt = datetime.now() #time at which the data was taken 
        #where shell ensures we're using shell to execute (TRUE IF ON WINDOWS), capture_output ensures stdout and stderr are captured, 
        #text ensures output captured and returned as a text string instead of bytes.

    def processData(self):
        self.processedCPUUtil = [float(self.__CPUrawGrep.stdout.split()[1]), self.__timeAt] #splits the __CPUrawGrep output, converts to float, then gets position 1 (X.X us value for % utilisation) + time and puts into a list
        return self.processedCPUUtil

    def __str__(self):
        return f"{self.processedCPUUtil}"

class UbuntuMemData:
    def __init__(self):
        self.__memRawData = subprocess.run(["top", "-b", "-n", "1"], stdout=subprocess.PIPE, shell=False, text=True) #get raw Ubuntu top Memory data
        self.__memRawGrep = subprocess.run(["grep", "MiB Mem"], input=self.__memRawData.stdout, shell=False, capture_output=True, text=True) #data gets piped into the grep command
        #output: MiB Mem :  16310.7 total,   8692.8 free,   7393.9 used,    224.0 buff/cache
        self.__timeAt = datetime.now() #time at which the data was taken

    def processData(self):
        self.__processedMemTotal = float(self.__memRawGrep.stdout.split()[3]) #splitting the __memRawGrep output, converting to float, then gets position 3 (total memory)
        self.__processedMemFree = float(self.__memRawGrep.stdout.split()[5]) #splitting + float conversion + gets position 5 (free memory)
        self.__processedResult = (1 - (self.__processedMemFree / self.__processedMemTotal)) * 100
        self.processedMemUtil = [f'{self.__processedResult:.1f}', self.__timeAt] #places them in a list to match the UbuntuCPUData.processData formatting (% total utilisation)
        return self.processedMemUtil

    def __str__(self):
        return f"{self.processedMemUtil}"
