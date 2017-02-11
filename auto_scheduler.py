import datetime
import json
import os
import requests
import smsapi
import sqlite3

from ESlave import *

NOW = datetime.datetime.today().weekday()
TESTING = False

def main():
    """Sunday shoutout! We spin up our virtual ESlave() butler named Charles,
    call on him to check the weather, check our mail server for responses from
    players, and if its Sunday sent out requests for player's weekly schedules.

    Requests for player's schedules only occurs on Sunday(or any day of
    your choosing),................yadda yadda yadda


    """
    Charles = ESlave()
    Charles.check_weather() #works
    Charles.check_mail() #works
    print "\n                ~~Weather and mail checked~~\n"
    NOW = datetime.datetime.today().weekday()

    if (NOW == 5 & TESTING == False): #Sunday=6, Monday = 0
        Charles.send_email_out()
        Charles.send_sms_out()
        print "\n                ~~E-mail and SMS-Text messages sent ~~\n"
    else:
        print "\n                ~~Done~~\n"


if __name__ == '__main__':
    main()
