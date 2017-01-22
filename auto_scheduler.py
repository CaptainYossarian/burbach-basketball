import datetime
import json
import os
import requests
import smsapi
import sqlite3

from ESlave import *


def main():
    """Sunday shoutout! We spin up our virtual ESlave() butler named Charles,
    call on him to check the weather, check our mail server for responses from
    players, and if its Sunday sent out requests for player's weekly schedules.

    Requests for player's schedules only occurs on Sunday(or any day of
    your choosing),................yadda yadda yadda


    """
    Charles = ESlave()
    #globals
    NOW = datetime.datetime.today().weekday()
    TEST_FLAG = False

    #loaded_flag = False for testing to not overuse free api calls

    if NOW == 0: #Sunday=6, Monday = 0
        Charles.check_weather()
        Charles.check_mail()

        if TEST_FLAG == False:
            Charles.send_email_out()
            #Charles.send_sms_out()
            print "\n                ~~Done, Boss.~~\n"
        else:
            print "\n~~No action taken~~\n"

if __name__ == '__main__':
    main()
