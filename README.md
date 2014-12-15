RPICatFeeder
============

Documentation
-----
My main website contains the inforatiom on building this cat feeder. 
http://drstrangelove.net/2013/12/raspberry-pi-power-cat-feeder-updates/

Info
-----

Raspberry Pi Cat Feeder Code Version 2.

This code is based on the python-rpi.gpio modules version >=0.5.4-1.

You might have to manually remove the old GPIO library to get this work.

This program also requires adding the following python modules:
* [astral] (https://pythonhosted.org/astral/module.html)
* [pytz] (http://pytz.sourceforge.net)
* [GPIO] (http://sourceforge.net/projects/raspberry-gpio-python/)

Installation
-----------
     sudo apt-get install python-pip
     sudo pip install astral
     sudo pip install pytz 
     sudo apt-get install python-rpi.gpio

Running
-------
You can run the main script (Cat-Feeder-Button-pwm.py) in a secreen/byobu or even by adding it to /etc/rc.local to start a boot.

Email setup
----------
To setup email, enter your info in the main program file for the server and what now, and then create a file named email_settings.py
Then add the following lines to the email_settings.py file:
email_to = 'youremailATyourdomain'
email_gmail_user = 'gmail or google apps userid'
email_gmail_pwd = 'gmail or google apps password'



