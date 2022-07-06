################ Henri Lahousse ##################
# connect to blynk interface, control onward by phone
# 6/1/2022

import blynklib #Import Blynk library
from motor import speed_down, stop, m_roof, m_front, m1, speed_up
from time import sleep

BLYNK_AUTH = 'CFa68mIWEDr_LO9ySslr1znQvcuEmWWF' #insert your blynk code from your blynk project
blynk = blynklib.Blynk(BLYNK_AUTH)


#WRITE_EVENT_PRINT_MSG = "[WRITE_VIRTUAL_PIN_EVENT] Pin: V{} Value: '{}'" 

# left
@blynk.handle_event('write V2')
def left(pin, value):
    #print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    #return value[0]
    val = int(value[0])
    print(pin, val)
    if val == 1:
       m_front(0)
       sleep(0.1)
    if val == 0:
       stop()

# right
@blynk.handle_event('write V3')
def right(pin, value):
    #print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    #return value[0]
    val = int(value[0])
    print(pin, val)
    if val == 1:
       m_front(val)
       sleep(0.1)
    if val == 0:
       stop()

# closes and opens roof, virtual pin V4
@blynk.handle_event('write V4')
def roof(pin, value):
    #print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    #return value[0]
    val = int(value[0])
    print(val)
    m_roof(val)
    sleep(31)
    stop()

spd = [0]

# collects speed from app and stores in speed list, virtual pin V5
@blynk.handle_event('write V5')
def speed(pin, value):
    #print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    #return value[0]
    sp = round(((int(value[0]))/2.55), 1) # the motor driver works with percentages so everything should be 2.55 times smaller
    print(sp)
    spd[0] = sp
    #print(spd)

# drive forwards,, virtual pin V0
@blynk.handle_event('write V0')
def forward(pin, value):
    #print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    #return value[0]
    print('speed: ', spd)
    val = int(value[0])
    print('forward', val)
    if val == 1:
       speed_up(0, 1, spd[0])
       m1(1, spd[0])
       sleep(0.1)
    if val == 0: 
       speed_down(0, 1)
       stop()

# drive backwards, virtual pin V1
@blynk.handle_event('write V1')
def backwards(pin, value):
    #print(WRITE_EVENT_PRINT_MSG.format(pin, value))
    #return value[0]
    val = int(value[0])
    print(val)
    if val == 1:
       m1(0, spd[0])
       sleep(0.1)
    if val == 0:
       stop()

    
# infinite loop that waits for event
while True:
    blynk.run()