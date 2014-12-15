RPICatFeeder
============

Raspberry Pi Cat Feeder Code Version 2.

You will need:

The most recent version of the GPIO library for python. 
 http://sourceforge.net/p/raspberry-gpio-python/wiki/Home/

This version does not need two GPIO modules to function.

This is based on the python-rpi.gpio modules version >=0.5.4-1.

You might have to manually remove the old GPIO library to get this work.

This program requires adding the following modules:
astral
pytz
GPIO

Installation
-----------
     sudo apt-get install python-pip
     sudo pip install astral
     sudo pip install pytz 
     sudo apt-get install python-rpi.gpio

Email setup
----------
To setup email, enter your info in the main program file, and then create a file named email_settings.py
Then add the following lines to the email_settings.py file:
email_to = 'youremailATyourdomain'
email_gmail_user = 'gmail or google apps userid'
email_gmail_pwd = 'gmail or google apps password'

You can run the main script (Cat-Feeder-Button-pwm.py) in a secreen/byobu or even by adding it to /etc/rc.local to start a boot.


