#!/usr/bin/env python
# ds18b20 tem sensor

import os
import glob
import time

#os.system('modprobe w1-gpoi');

baseDir = '/sys/bus/w1/devices/';
deviceDir = glob.glob(baseDir + '28*')[0];
deviceFile = deviceDir + '/w1_slave';

class DS18B20:
    tempC = 0;
    tempF = 0;
    def __init__(self):
        self.tempC = 0;
        self.tempF = 0;
    # end init
        
    def readTempDevices(self):
        return glob.glob(baseDir + "28*");
    # end readTempDevices 

    def readTempRaw(self):
        f = open(deviceFile, 'r');
        lines = f.readlines();  # get all lines
        f.close();

        return lines;
    # end readTempRaw
    
    def readTemp(self):
        allLines = self.readTempRaw();

        while allLines[0].strip()[-3:] != 'YES':
            time.sleep(0.2);
            allLines = self.readTempRaw();
        # end while

        equalPos = allLines[1].find('t=');
        if equalPos != -1:
            tempStr = allLines[1][equalPos+2:];
            tempC = round(float(tempStr) / 1000.0,2);
            tempF = tempC * 9.0 / 5.0 + 32.0
        # end if

        #return tempC, tempF;
        return tempC;
    # end readTemp
# end DS18B20
