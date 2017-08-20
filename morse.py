#!/usr/bin/env python3
import sys
import logging
import ev3dev
import ev3dev.core
import time
 
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)5s: %(message)s')
logger = logging.getLogger(__name__)
ts = ev3dev.core.TouchSensor()


DOT_TIME=0.5
DASH_TIME=1.3
NO_ACTION_WAIT=1.0


last_press_time = time.time()
last_release_time = time.time()
last_press_state = False
already_send_when_quiet = False
string = ""
MORSE_CODE = {
    "._" : "A",
    "_..." : "B",
    "_._." : "C",
    "_.." : "D",
    "." : "E",
    ".._." : "F",
    "__." : "G",
    "...." : "H",
    ".." : "I",
    ".___" : "J",
    "_._" : "K",
    "._.." : "L",
    "__" : "M",
    "_." : "N",
    "___" : "O",
    ".__." : "P",
    "__._" : "Q",
    "._." : "R",
    "..." : "S",
    "_" : "T",
    ".._" : "U",
    "..._" : "V",
    ".__" : "W",
    "_.._" : "X",
    "_.__" : "Y",
    "__.." : "Z"  

}
def process (str):
    code = ""
    if str in MORSE_CODE.keys():
        code = MORSE_CODE[str]
        #print(str, code)
        sys.stdout.write(code)
        sys.stdout.flush()
    else:
        print(str)


print ("Lets start!")
while True:
    if ts.is_pressed:
        if not last_press_state:
            last_press_state = True
            last_press_time = time.time()
            already_send_when_quiet = False
            #logger.info("Pressed %s"% last_press_time)
    else:
        message = ""
        if last_press_state:
            last_press_state= False
            pressed_time = time.time() - last_press_time
            last_release_time = time.time()
            if pressed_time <= DOT_TIME:
                message = "."
            elif pressed_time <= DASH_TIME:
                message = "_"
            else:
                message = " "
                
            #logger.info("Popup %s %s"% (message,pressed_time))
        else:
            if time.time() - last_release_time > NO_ACTION_WAIT and not already_send_when_quiet:
                message = " "
                already_send_when_quiet = True
        if message != "":
            if message == " ":
                process(string)
                string = ""
            elif len(string) <= 3:
                string += message
                
            else:
                process(string)
                string = message
            
    time.sleep(0.1)