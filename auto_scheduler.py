import datetime
import json
import os
import requests
import smsapi
import sqlite3

from ESlave import *

NOW = datetime.datetime.today().weekday()
TESTING = True

def main():
    """Sunday shoutout! We spin up our virtual ESlave() butler named Charles,
    call on him to check the weather, check our mail server for responses from
    players, and if its Sunday sent out requests for player's weekly schedules.

    Requests for player's schedules only occurs on Sunday(or any day of
    your choosing),................yadda yadda yadda


    """

    Charles = ESlave()
    Charles.check_weather() #works
    print "\n                ~~Weather checked~~\n"
    Charles.check_mail() #works
    print "\n                ~~Mail checked~~\n"

    if (NOW == 5 and TESTING == False): #Sunday=6, Monday = 0
        Charles.send_email_out()#works
        Charles.send_sms_out()#works
        print "\n            ~~E-mail and SMS-Text messages sent ~~\n"
    else:
        print "\n                ~~Done~~\n"


if __name__ == '__main__':
    main()
