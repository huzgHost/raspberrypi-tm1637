#!/usr/bin/env python
# show temp in tm1637

import tm1637
import sys
#sys.path.insert(0, '/home/pi/git/raspberrypi-tm1637/sensor')
#import ds18b20
from sensor.ds18b20 import * 
import RPi.GPIO as GPIO
import time

CLK = 23
DATA = 24
GPIO.setmode(GPIO.BCM);
GPIO.setwarnings(False);

try:
    digital = tm1637.TM1637(CLK, DATA);
    digital.showDoublePoint(1);

    lastTemp = 0;
    while(True):
        #tempDS18b20 = ds18b20.DS18B20();
        tempDS18b20 = DS18B20();
        temp = tempDS18b20.readTemp();
        print 'temp :', temp
        realTemp = int(temp * 100);
        first = realTemp/1000%10;
        second = realTemp/100%10;
        third = realTemp/10%10;
        forth = realTemp%10;
        #print 'realTemp=', realTemp, first, ',', second, ',', third, ',', forth;
        number = [first, second, third, forth];
        digital.showData(number);

        time.sleep(0.5);
    # end while
except KeyboardInterrupt:
    pass

GPIO.cleanup();
