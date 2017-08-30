import RPi.GPIO as GPIO
import time

AOUT = 25;
OUT = GPIO.OUT;
IN = GPIO.IN;
LOW = GPIO.LOW;
HIGH = GPIO.HIGH;

GPIO.setmode(GPIO.BCM);
GPIO.setup(AOUT, IN, pull_up_down=GPIO.PUD_DOWN);

def analogRead():
	GPIO.setup(AOUT, OUT);
	GPIO.output(AOUT, LOW);
	time.sleep(0.005);

	GPIO.setup(AOUT, IN);
	count = 0;
	while not GPIO.input(b_pin):
		count = count + 1;

	return count;

def action(pin):
	#print 'sensor dected action:', analogRead();
	print 'sensor dected action';
	

#end action

try:
	#GPIO.add_event_detect(AOUT, GPIO.RISING, callback=action);	
	GPIO.add_event_detect(AOUT, GPIO.RISING);
	GPIO.add_event_callback(AOUT, callback=action);
	while True:
		print 'alive';
		time.sleep(1);
except KeyboardInterrupt:
	print "bye";	

GPIO.cleanup();
