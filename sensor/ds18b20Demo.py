#!/usr/bin/env python
# show status

import ds18b20

while True:
    tempDevice = ds18b20.DS18B20();

    print 'temp=', tempDevice.readTemp();
