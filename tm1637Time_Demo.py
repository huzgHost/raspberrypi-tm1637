#!/usr/bin/env python
# tm1637 test
# show cur timer

import tm1637
import RPi.GPIO as GPIO
import time

CLK = 23;
DATA  = 24;
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False);

HHMMFORMAT = '%H:%M'

try:    
    digital1637 = tm1637.TM1637(CLK, DATA)
    digital1637.showDoublePoint(1);
    
    lastTime = 0;
    while(True):
        curTime = time.strftime(HHMMFORMAT, time.localtime(time.time()));
        if(curTime != lastTime):
            print 'time is not equ, change timer, curTime = ', curTime, 'lastTime=', lastTime;
            timer = time.localtime();
            number = [timer.tm_hour/10, timer.tm_hour%10, timer.tm_min/10, timer.tm_min%10];
            digital1637.showData(number);
            lastTime = curTime;
        # end if

        time.sleep(0.05);
    # end while
    
except KeyboardInterrupt:
    pass

GPIO.cleanup();
