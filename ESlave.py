import ConfigParser
import datetime
import email
import imaplib
import os
import json
import requests
import smtplib
import smsapi

from twilio.rest import TwilioRestClient

#set myconfig file path. create a SafemyconfigParser. load 'myconfig'.txt INI file
configfile = "/home/drg/cs/pycode/Burbach/burbach.config.txt"
myconfig = ConfigParser.SafeConfigParser()
myconfig.read(configfile)

#set myconfig variables from 'myconfig'.txt. tuple1 = myconfig section. tuple2 = myconfig value
FROM = myconfig.get('misc','FROM')
GUSER_NAME = myconfig.get('misc','GUSER_NAME')
GPASS = myconfig.get('misc','GPASS')
OUTPUT_DIRECTORY = myconfig.get('misc','OUTPUT_DIRECTORY')
TO = myconfig.get('misc','TO')
TESTMESS = myconfig.get('misc','TESTMESS')


class ESlave(object):
        """A virtual butler who does our bidding"""

        def __init__(self):
            """
            Args:
                GUSER_NAME = gmail username specified in your myconfig
                GPASS = a gmail password specified in your myconfig

            """
            self.guser_name = GUSER_NAME
            self.gpass = GPASS

        def send_email_out(self):
            """Sends an email from an ESlave object TO all recpients via SMTP_SSL on port 465
            (once account is allowed access under the gmail preferences.)

            """

            print("~~Your wish is my command. Sending E-mail out!")
            server_ssl = smtplib.SMTP_SSL("smtp.gmail.com",465)
            server_ssl.ehlo()
            server_ssl.login(self.guser_name, self.gpass)
            server_ssl.sendmail(FROM, TO, TESTMESS)
            print("~~E-mail sent.")

        def send_sms_out(self):
            """Sends a text sms out to a recipient. Uses TwilioRestClient.

            Note: myconfig.get(___,___) pulls values from your myconfig file via
            a SafemyconfigParser named myconfig.

            """

            print "~~Your wish is my command. Sending SMS-Texts out!"
            ACCOUNT_SID = myconfig.get('twilio','ACCOUNT_SID')
            AUTH_TOKEN = myconfig.get('twilio','AUTH_TOKEN')

            twilio_number = myconfig.get('twilio','twilio_number')
            my_cell = myconfig.get('twilio','my_cell')
            body = myconfig.get('twilio','body')

            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(to=my_cell,from_=twilio_number,body=body)
            print "~~Text messages sent."

        def check_mail(self):
            """Logs into a mail account. Checks the messages. Opens and
            processes the boxes

            """
            host = imaplib.IMAP4_SSL('imap.gmail.com')
            _gmail_connect(host)
            _query_boxes(host)
            _open_box(host, "inbox")
            _process_mailbox(host)

        def check_weather(cls):
            """Gets weather information from the Openweather API
            for the coming week(currently displays for one day only) and prints.

            """
            cls.owm_key = myconfig.get('weather','cls.owm_key')
            cls.fairfax = myconfig.get('weather','cls.fairfax')

            url = "http://api.openweathermap.org/data/2.5/weather?id=5347322&APPID=2b5d9c4fe3c6417dfc18b1aa9a3f1974&units=imperial"
            r = requests.get(url)
            p = r.json()
            q = json.loads(json.dumps(p))
            _weather_report(q)

#Helper methods to ESlave()
def _weather_report(jstream):
    """Prints relevant weather information in a pre-arranged order.

    Args:
        jstream = json stream

    """
    print "\nThe temperature in %s on %s is:\n" % (jstream.get('name'), datetime.date.today())
    print "High: %d | Low: %d " % (jstream.get('main').get('temp_max'),jstream.get('main').get('temp_min'))
    print "Rain: '%r' inches" %  jstream.get('rain')
    print "Wind Speed: %s mph\n" % jstream.get('wind').get('speed')

def _gmail_connect(M):
    """Logs into gmail.

    Args:
        M =  imap connection
        user_name = gmail user name (use GUSER_NAME from myconfig)
        password = gmail password (use GPASS from myconfig)
    Raises:
        IMAP4.error: for failed login/bad credentials

    """
    try:
        M.login("novabasketballscheduler","joeandfriends34")
        print "~~connection established with {0} ~~".format(GUSER_NAME)
    except imaplib.IMAP4.error:
        print "~~login failed ~~"


def _query_boxes(M):
    """Checks the available boxes and prints them.

    Args:
        M =  imap connection

    """
    response, mailboxes = M.list()
    if response == 'OK':
       print "Mailboxes:"
       print mailboxes

def _open_box(M, which_box):
    """Selects which box on an email client to perform operations on and opens it.

    Args:
        M - imap connection
        which_box - which box to perform operations on

    """
    response = M.select(which_box)
    if response == "OK":
        print "~~Processing selected box"
            #M.close()

def _process_mailbox(M):
    """Returns the datetime and and payload for the box

       M = imap connection

    """
    print "Messages:"
    rv, kys = M.search(None,"ALL")
    if rv != 'OK':
        print "~~No messages found!"
        return

    for num in kys[0].split():
        rv, kys = M.fetch(num, '(RFC822)')
        if rv != 'OK':
            print "~~ERROR getting message", num
            return

        msg = email.message_from_string(kys[0][1])
        print 'Message %s: %s' % (num, msg['Subject'])
        print 'Raw date:', msg['Date']
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(
                email.utils.mktime_tz(date_tuple))
            print "Local Date:", \
                    local_date.strftime("%a, %d %b %Y %H:%M:%S")
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                print part.get_payload()
