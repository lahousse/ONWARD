############### Henri Lahousse #################


# library
from sqlite3 import Time
import RPi.GPIO as GPIO			       # RPi GPIO module
from time import sleep			       # for the delays


GPIO.setmode(GPIO.BCM)			# GPIO numbering
GPIO.setwarnings(False)			# enable warning from GPIO

# outputs
AN1 = 19                # pwm pin dc motor 
AN_front = 12			    	# pwm pin lineaire motor steering
AN_roof = 13	     	   	# pwm pin lineaire motor roof
AN_led = 18             # pwm pin led
DIG1 = 26               # digitale pin dc motor 
DIG_front = 5				    # digitale pin lineaire motor steering
DIG_roof = 6            # digitale pin led
DIG_led = 17


# setup GPIO
GPIO.setup(AN1, GPIO.OUT)		      # pin as output
GPIO.setup(AN_front, GPIO.OUT)    # =
GPIO.setup(AN_roof, GPIO.OUT)     # =
GPIO.setup(AN_led, GPIO.OUT)      # =
GPIO.setup(DIG1, GPIO.OUT)		    # =
GPIO.setup(DIG_front, GPIO.OUT)   # =
GPIO.setup(DIG_roof, GPIO.OUT)    # =
GPIO.setup(DIG_led, GPIO.OUT)     # =


# pwm frequentie
pwm = 10000

sleep(1)

p1 = GPIO.PWM(AN1, pwm)		           # setup pwm M1
p_front = GPIO.PWM(AN_front, pwm)    # setup pwm M_front
p_roof = GPIO.PWM(AN_roof, pwm)		   # setup pwm M_roof
p_led = GPIO.PWM(AN_led, pwm)		     # setup pwm led

def m1(d, sp):
    if d == 0:
       GPIO.output(DIG1, GPIO.HIGH)		# 0 = backwards
       p1.start(sp)				            # speed
 
    if d == 1:
       GPIO.output(DIG1, GPIO.LOW)		# 1 = forward
       p1.start(sp)				            # speed



def m_front(d): # d(direction): 0 = left, 1 = right
    sp = 100
    if d == 0:
       GPIO.output(DIG_front, GPIO.HIGH)		# left
       p_front.start(sp)				            # speed

    if d == 1:
       GPIO.output(DIG_front, GPIO.LOW)		 # right
       p_front.start(sp)				           # speed


def m_roof(d, delay):
    sp = 100
    if d == 1:
       GPIO.output(DIG_roof, GPIO.LOW)		# up (31 sec to fully open roof)
       p_roof.start(sp)				            # speed

    if d == 0:
       GPIO.output(DIG_roof, GPIO.HIGH)		# down
       p_roof.start(sp)				            # speed

    sleep(delay)

def led():
   print('led on')
   sp = 100
   GPIO.output(DIG_led, GPIO.LOW)		
   p_led.start(sp)
  

# stop for every motor individually
def stop_m1():
   GPIO.output(DIG1, GPIO.LOW)	
   p1.stop()

def stop_mfront():
   GPIO.output(DIG_front, GPIO.LOW)
   p_front.stop()	

def stop_mroof():
   GPIO.output(DIG_roof, GPIO.LOW)
   p_roof.stop()

def stop_led():
   GPIO.output(DIG_led, GPIO.LOW)
   p_led.stop()

# stopt all motors
def stop():
   GPIO.output(DIG1, GPIO.LOW)	
   GPIO.output(DIG_front, GPIO.LOW)
   GPIO.output(DIG_roof, GPIO.LOW)	
   GPIO.output(DIG_led, GPIO.LOW)	
   p1.stop()	
   p_roof.stop()
   p_front.stop()	
   p_led.stop()		


motoren = [m1, m_front, m_roof, ]

# function to speed motor up
def speed_up(motor, direction, max):
   n = 0
   while n < max:
      print(n)
      #print('max', mx[0], 'now', n)
      motoren[motor](direction, n)
      sleep(0.1)
      n+=1

   #sleep(time)

# function to speed motor down
def speed_down(motor, direction, max):
   n = max
   while n > 15:
      print('speeding down', n)
      motoren[motor](direction, n)
      sleep(0.1)
      n -= 1
