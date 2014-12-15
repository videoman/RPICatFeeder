#!/usr/bin/env python
#
# Example for Hack Factory Raspberry Pi Class.
# David M. N. Bryan, dave@drstrangelove.net
#
# This is licenced under creative commons license:
# http://creativecommons.org/licenses/by-nc-sa/3.0/
# Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)

# It's a timeywimey thing.
import time

#Grab the SMTP library
import smtplib
# This file conttains email_to, email_gmail_user, and email_gmail_pwd
from email_settings import *

# We need to be able to tell time for the cats.
import datetime 

from datetime import date, timedelta, datetime

# Import the Raspberry Pi GPIO library.
import RPi.GPIO as GPIO

#Astral will tell us when the sun sets, and that's when we want to feed the kitties
from astral import *
from pytz import timezone

#Setup the location and lat/lon for our calculations
a = Astral()
location = a['Minneapolis']

# Setup the Email stuff.
def send_email(feedtime):
  feedtime = feedtime.strftime("%a %b %m at %I:%M%p")
  d2 = datetime.today() + timedelta(days=1)
  tomorrowfeedtime = location.dusk(local=True, date=d2)
  tomorrowfeedtime = tomorrowfeedtime.strftime("%a %b %m at %I:%M%p")
  to = email_to
  gmail_user = email_gmail_user
  gmail_pwd = email_gmail_pwd
  smtpserver = smtplib.SMTP("smtp.gmail.com",587)
  smtpserver.ehlo()
  smtpserver.starttls()
  smtpserver.ehlo
  smtpserver.login(gmail_user, gmail_pwd)
  header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject: CatFeeder: I fed the cats on ' + feedtime + '\n'
  #print header
  msg = header + '\n I fed the cats on ' + feedtime + ' today.\n\nTomorrow I will fed the cats on ' + tomorrowfeedtime + '\n\n'
  print msg
  smtpserver.sendmail(gmail_user, to, msg)
  print 'email sent!'
  smtpserver.close()

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

# Setup the Servos Pins
GPIO.setup(Servo1Pin, GPIO.OUT)
GPIO.setup(Servo2Pin, GPIO.OUT)

# I'm going to make some functions that do the servo rotation, 
# so I don't have to change a ton of code later on if I need to.

# This rotates the feeder wheel Clock Wise (from left to right)
def servo_CW(ServoPIN,SleepTime):
  # Set servo on Servo1Pin to 1200us (1.2ms)
  servo = GPIO.PWM(ServoPIN, 50)
  servo.start(10.5)
  time.sleep(SleepTime)
  servo.stop()
  time.sleep(.05)

# This rotates both feeder wheels Clock Wise (from left to right)
# at the same time
def dual_servo_CW(Servo1PIN,Servo2PIN,SleepTime):
  # Set servo on Servo1Pin to 1200us (1.2ms)
  # This rotates the servo CW.
  servo1 = GPIO.PWM(Servo1PIN, 50)
  servo2 = GPIO.PWM(Servo2PIN, 50)
  servo1.start(10.5)
  servo2.start(10.5)
  time.sleep(SleepTime)
  servo1.stop()
  servo2.stop()

# This rotates the feeder wheel Counter Clock Wise (from right to left)
def servo_CCW(ServoPIN,SleepTime):
  # Set servo on Servo1Pin to 2000s (2.0ms)
  #servo.set_servo(ServoPIN, 2000)
  servo = GPIO.PWM(ServoPIN, 50)
  servo.start(4.5)
  time.sleep(SleepTime)
  # Clear servo on Servo1Pin
  servo.stop()
  #time.sleep(.25)

# This rotates both feeder wheels Counter Clock Wise (from right to left)
# at the same time
def dual_servo_CCW(Servo1PIN,Servo2PIN,SleepTime):
  # Set servo on Servo1Pin to 2000us (2.0ms)
  servo1 = GPIO.PWM(Servo1PIN, 50)
  servo2 = GPIO.PWM(Servo2PIN, 50)
  servo1.start(4.5)
  servo2.start(4.5)
  time.sleep(SleepTime)
  servo1.stop()
  servo2.stop()

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
     servo_CCW(Servo2Pin,FeedTime)

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

# The 1.3 second delay time is about 1/2C of food
#  YMMV depending on the feeder.
def feed_cat(CatName):
  if (CatName == "Thor"):
    feed_thing("Right",1.01)
    time.sleep(.25)

  if (CatName == "Zelda"):
    feed_thing("Left",1.01)
    time.sleep(.25)

# This setup is to feed the cat at a specific time.
def feed_time(Feed_hour,Feed_minute):
  if time.strftime("%H") == "Feed_hour" and time.strftime("%M") == "Feed_minute":
    print "Cat Feeing time!"
    feed_cat("Zelda")
    time.sleep(1.5)
    feed_cat("Thor")
    time.sleep(60)

def LeftFeedButton(GPIO_ButtonL_PIN):
  feed_cat("Zelda")

def RightFeedButton(GPIO_ButtonR_PIN):
  feed_cat("Thor")

def whenisdusk():
  dusk = location.dusk(local=True, date=None)
  #dusk = datetime.now()
  #dusk2 = dusk.replace(tzinfo=None)
  dusk2 = dusk.strftime("%Y-%m-%d %H:%M:%S")
  return dusk2

# This works great if you don't have any static-electricty in the enviroment.
# This function will detect when the button is pushed, and call the approiate function.
GPIO.add_event_detect(GPIO_ButtonL_PIN, GPIO.RISING, callback=LeftFeedButton, bouncetime=500)
GPIO.add_event_detect(GPIO_ButtonR_PIN, GPIO.RISING, callback=RightFeedButton, bouncetime=500)

# Set the initial dusk time
dusk = whenisdusk()

# First off, lets turn the LEDs for the buttons on!
GPIO.output(GPIO_ButtonL_LED_PIN, True)
GPIO.output(GPIO_ButtonR_LED_PIN, True)

# This is the main loop where we wait for stuff to happen!
while True:
  # What time is it?
  now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  # We set the dusk time really early this morning. If it's true, then we should feed the casts.
  if now == dusk:
    # Setting a varaible to use when we send email about what time we fed the cats.
    feedtime=datetime.now(timezone('US/Central'))
    print "Cat Feeding time %s" % feedtime.strftime("%Y-%m-%d %H:%M:%S")
    # Call the function "feed_cat" to feed the cats.
    feed_cat("Zelda")
    feed_cat("Thor")
    send_email(feedtime)
    time.sleep(60)

  #Manual single time feed - set at a specific time
  #if time.strftime("%H") == "19" and time.strftime("%M") == "01" and time.strftime("%S") == "01":
  #  feedtime=datetime.now(timezone('US/Central'))
  #  print "Cat Feeding time %s" % feedtime.strftime("%Y-%m-%d %H:%M:%S")
  #  feed_cat("Zelda")
  #  feed_cat("Thor")
  #  send_email(feedtime)
  #  time.sleep(60)

  #Update the dusk time each day
  if time.strftime("%H") == "03" and time.strftime("%M") == "01" and time.strftime("%S") == "01":
    dusk = whenisdusk()

#  If nothing to do, go back to the loop... forever...
  time.sleep(1)
