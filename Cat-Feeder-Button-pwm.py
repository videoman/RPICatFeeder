#!/usr/bin/env python
#
# Example for Hack Factory Raspberry Pi Class.
# David M. N. Bryan, dave@drstrangelove.net
#
# This is licend under creative commons license:
# http://creativecommons.org/licenses/by-nc-sa/3.0/
# Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

# Import the PWM library so we can control the servos.
from RPIO import PWM

# It's a timeywimey thing.
import time

# We need to be able to tell time for the cats.
import datetime 

# Import the Raspberry Pi GPIO library.
import RPi.GPIO as GPIO

# I have the Servero input ping (White wires) setup
# for the fllowing pins
Servo1Pin=18
Servo2Pin=23

# I have a pizeo beeper to announce when I'm going to 
# hurl food at you.  puny human.
BeeperPin=24

# Left Switch has an LED pin, and a Switch input pin
GPIO_ButtonL_LED_PIN=4
GPIO_ButtonL_PIN=17

# Right Switch has an LED pin, and a Switch input pin
GPIO_ButtonR_LED_PIN=27
GPIO_ButtonR_PIN=22

# Tell the GPIO who is what,EG: OUTPUTS , beeper, LEDS, inputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(BeeperPin, GPIO.OUT)
GPIO.setup(GPIO_ButtonL_LED_PIN, GPIO.OUT)
GPIO.setup(GPIO_ButtonL_PIN, GPIO.IN)
GPIO.setup(GPIO_ButtonR_LED_PIN, GPIO.OUT)
GPIO.setup(GPIO_ButtonR_PIN, GPIO.IN)

# Set the beeper&LED pins low, so they don't light or sweek on boot.
GPIO.output(BeeperPin, False)
GPIO.output(GPIO_ButtonL_LED_PIN, False)
GPIO.output(GPIO_ButtonR_LED_PIN, False)

# Setup the servo PWM library
servo = PWM.Servo()

# I'm going to make some functions that do the servo rotation, 
# so I don't have to change a ton of code later on if I need to.

# This rotates the feeder wheel Clock Wise (from left to right)
def servo_CW(ServoPIN,SleepTime):
  # Set servo on Servo1Pin to 1200us (1.2ms)
  servo.set_servo(ServoPIN, 1200)
  time.sleep(SleepTime)
  servo.stop_servo(ServoPIN)
  time.sleep(.25)

# This rotates both feeder wheels Clock Wise (from left to right)
# at the same time
def dual_servo_CW(Servo1PIN,Servo2PIN,SleepTime):
  # Set servo on Servo1Pin to 1200us (1.2ms)
  # This rotates the servo CW.
  servo.set_servo(Servo1PIN, 1200)
  servo.set_servo(Servo2PIN, 1200)
  time.sleep(SleepTime)
  servo.stop_servo(Servo1PIN)
  servo.stop_servo(Servo2PIN)
  #time.sleep(.25)

# This rotates the feeder wheel Counter Clock Wise (from right to left)
def servo_CCW(ServoPIN,SleepTime):
  # Set servo on Servo1Pin to 2000s (2.0ms)
  servo.set_servo(ServoPIN, 2000)
  time.sleep(SleepTime)
  # Clear servo on Servo1Pin
  servo.stop_servo(ServoPIN)
  #time.sleep(.25)

# This rotates both feeder wheels Counter Clock Wise (from right to left)
# at the same time
def dual_servo_CCW(Servo1PIN,Servo2PIN,SleepTime):
  # Set servo on Servo1Pin to 1200us (1.2ms)
  servo.set_servo(Servo1PIN, 2000)
  servo.set_servo(Servo2PIN, 2000)
  time.sleep(SleepTime)
  servo.stop_servo(Servo1PIN)
  servo.stop_servo(Servo2PIN)
  #time.sleep(.25)

# I created a function to feed the "thing" from the approiate side, based
# on the user input.  This function calls the servo funcations.
def feed_thing(HopperSide,FeedTime):
   if(HopperSide == "Left"):
     GPIO.output(GPIO_ButtonL_LED_PIN, False)
     GPIO.output(BeeperPin, True)
     time.sleep(.10)
     GPIO.output(BeeperPin, False)
     GPIO.output(GPIO_ButtonL_LED_PIN, True)
     print "Ok, food is coming out the left bin!"
     servo_CW(Servo1Pin,FeedTime)

   if(HopperSide == "Right"):
     GPIO.output(GPIO_ButtonR_LED_PIN, False)
     GPIO.output(BeeperPin, True)
     time.sleep(.10)
     GPIO.output(BeeperPin, False)
     GPIO.output(GPIO_ButtonR_LED_PIN, True)
     print "Ok, food is coming out the right bin!"
     servo_CW(Servo2Pin,FeedTime)

   if(HopperSide == "Both"):
     GPIO.output(GPIO_ButtonL_LED_PIN, False)
     GPIO.output(GPIO_ButtonR_LED_PIN, False)
     GPIO.output(BeeperPin, True)
     time.sleep(.25)
     GPIO.output(BeeperPin, False)
     time.sleep(.25)
     GPIO.output(BeeperPin, True)
     time.sleep(.25)
     GPIO.output(BeeperPin, False)
     time.sleep(.25)
     GPIO.output(BeeperPin, True)
     time.sleep(.25)
     GPIO.output(BeeperPin, False)
     GPIO.output(GPIO_ButtonL_LED_PIN, True)
     GPIO.output(GPIO_ButtonR_LED_PIN, True)
     print "Ok, food is coming out at both ends!"
     #servo_CCW(Servo2Pin,FeedTime)
     dual_servo_CW(Servo1Pin,Servo2Pin,FeedTime)

# Lets send out two beeps so that the user knows that we are ready to 
# dispense some food.
GPIO.output(BeeperPin, True)
time.sleep(.25)
GPIO.output(BeeperPin, False)
time.sleep(.25)
GPIO.output(BeeperPin, True)
time.sleep(.25)
GPIO.output(BeeperPin, False)

def feed_cat(CatName):
  if (CatName == "Thor"):
    feed_thing("Right",1.3)
    time.sleep(.25)
#    feed_thing("Right",.5)
#    time.sleep(.25)
#    feed_thing("Right",.5)
#    time.sleep(.25)
#    feed_thing("Right",.5)

  if (CatName == "Zelda"):
    feed_thing("Left",1.3)
    time.sleep(.25)
#    feed_thing("Left",.8)
#    time.sleep(.25)
#    feed_thing("Left",.5)
#    time.sleep(.25)
#    feed_thing("Left",.5)

def feed_time(Feed_hour,Feed_minute):
  if time.strftime("%H") == "Feed_hour" and time.strftime("%M") == "Feed_minute":
    print "Cat Feeing time!"
    feed_cat("Zelda")
    time.sleep(1.5)
    feed_cat("Thor")
    time.sleep(60)

# This is the main loop where we wait for stuff to happen!
while True:
  #now = datetime.datetime.now()
  #print now.time()
  time.sleep(1)

  # First off, lets turn the LEDs for the buttons on!
  GPIO.output(GPIO_ButtonL_LED_PIN, True)
  GPIO.output(GPIO_ButtonR_LED_PIN, True)

  # Now lets evaluate if a button is bushed...
  # If both buttons are pushed, call the feed_thing function, feeding both hoppers for X seconds.
  if ( GPIO.input(GPIO_ButtonL_PIN) == True and GPIO.input(GPIO_ButtonR_PIN) == True ):
    feed_thing("Both",2)

  # If only the left button is pushed, feed from the left hopper for half a second.
  elif ( GPIO.input(GPIO_ButtonL_PIN) == True ):
    feed_cat("Zelda")

  # If only the right button is pushed, feed from the right hopper for half a second.
  elif ( GPIO.input(GPIO_ButtonR_PIN) == True ):
    feed_cat("Thor")

  #feed_time("22","10")
  #if time.strftime("%H") == "20" and time.strftime("%M") == "30":
  #  print "Cat Feeing time!"
  #  feed_cat("Zelda")
  #  time.sleep(.5)
  #  feed_cat("Thor")
  #  time.sleep(60)
 
  if time.strftime("%H") == "10" and time.strftime("%M") == "30":
    print "Cat Feeing time!"
    feed_cat("Zelda")
    time.sleep(.5)
    feed_cat("Thor")
    time.sleep(60)

#  If nothing to do, go back to the loop... forever...
