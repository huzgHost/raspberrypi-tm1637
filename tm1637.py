#!/usr/bin/env python
# tm1637 class

import time
import RPi.GPIO as GPIO

# 0, 1, 2, 3, 4, 5, 6, 7, 8 ,9
#HexDigits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f,0x77,0x7c,0x39,0x5e,0x79,0x71];
HexDigits = [0x3f,0x06,0x5b,0x4f,0x66,0x6d,0x7d,0x07,0x7f,0x6f];

ADDR_AUTO = 0x40;
ADDR_FIXED = 0x44;
START_ADDR = 0xC0;
BRIGHT_DARKEST = 0;
BRIGHT_TYPICAL = 2; 
BRIGHT_HIGHEST = 7;
OUTPUT = GPIO.OUT;
INPUT = GPIO.IN;
LOW = GPIO.LOW;
HIGH = GPIO.HIGH;

class TM1637:
    doublePoint = False;
    clkPin = 0;
    dataPin = 0;
    brightnes = BRIGHT_TYPICAL;
    curData = [0, 0, 0, 0];

    def __init__(self, clkPin, dataPin, brightnes = BRIGHT_TYPICAL):
        self.clkPin = clkPin;
        self.dataPin = dataPin;
        self.brightnes = brightnes;
        GPIO.setup(self.clkPin, OUTPUT);
        GPIO.setup(self.dataPin, OUTPUT);
    # end __init__

    def clear(self):
        point = self.doublePoint;
        self.doublePoint = False;
        data = [0, 0, 0, 0];
        self.showData(data);
        self.doublePoint = point;
    # end clear

    def showData(self, data):
        #print 'show data';
        for i in range(0, 4):
            self.curData[i] = data[i];
            #print 'data[', i, ']', data[i];
        #end for

        self.start();
        self.writeByte(ADDR_AUTO);
        self.stop();
        self.start();
        self.writeByte(START_ADDR);
        for i in range(0, 4):
            self.writeByte(self.encode(data[i]));
        self.stop()
        self.start();
        self.writeByte(0x88 + self.brightnes);
        self.stop();
    # end showData

    def showDoublePoint(self, on):
        if(self.doublePoint != on):
            self.doublePoint = on;
            self.showData(self.curData);
        # end if
    #end showDoublePoint

    def writeByte(self, data):
        for i in range(0, 8):
            GPIO.output(self.clkPin, LOW);
            if(data & 0x01):
                GPIO.output(self.dataPin, HIGH);
            else:
                GPIO.output(self.dataPin, LOW);

            data = data >> 1;
            GPIO.output(self.clkPin, HIGH);
        # end for

        # wait for ACK
        GPIO.output(self.clkPin, LOW);
        GPIO.output(self.dataPin, HIGH); # set data gpio high, util slave ack,set low
        GPIO.output(self.clkPin, HIGH);
        GPIO.setup(self.dataPin, INPUT); # set data gpio to input for slave

        #print 'self.dataPint = ', self.dataPin;

        while(GPIO.input(self.dataPin)):
            time.sleep(0.001);
            if(GPIO.input(self.dataPin)):
                GPIO.setup(self.dataPin, OUTPUT);
                GPIO.output(self.dataPin, LOW);
                GPIO.setup(self.dataPin, INPUT);
            # end if
        # end while
        #print 'ack is get'
        GPIO.setup(self.dataPin, OUTPUT);

    # end writeByte
    
    def start(self):
        GPIO.output(self.clkPin, HIGH);
        GPIO.output(self.dataPin, HIGH);
        GPIO.output(self.dataPin, LOW);
        GPIO.output(self.clkPin, LOW)
    # end start
    
    def stop(self):
        GPIO.output(self.clkPin, LOW);
        GPIO.output(self.dataPin, LOW); 
        GPIO.output(self.clkPin, HIGH);
        GPIO.output(self.dataPin, HIGH);
    # end stop

    def encode(self, data):
        if(self.doublePoint):
            pointData = 0x80;
        else:
            pointData = 0;

        if(data == 0x7F):
            data = 0;
        else:
            data = HexDigits[data] + pointData;

        return data;
    # end encode

# end class TM1637

