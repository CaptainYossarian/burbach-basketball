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

#config file points to the filepath of your local config file. see the sample
#for more details on how to configure
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
            """

        def check_mail(self):
            """Logs into a mail account. Checks the messages. Opens and
            processes the boxes

            """
            connection = imaplib.IMAP4_SSL('imap.gmail.com')
            _gmail_login(connection)
            #Runs if there are new messages. [None]returned = no new messages
            if (connection.recent() != ('OK',[None]) ):
                print "~~checking messages, downloading new messages~~"
                _check_boxes(connection)
                _open_box(connection,"inbox")
                #process_mailbox(host) #does not work
        def check_weather(cls):
            """Gets weather information from the Openweather API
            for the coming week(currently displays for one day only) and prints.

            """
            owm_key = myconfig.get('weather','owm_key')
            fairfax = myconfig.get('weather','fairfax')

            url = "http://api.openweathermap.org/data/2.5/weather?id=5347322&APPID=2b5d9c4fe3c6417dfc18b1aa9a3f1974&units=imperial"
            geturl = requests.get(url)
            getjson = geturl.json()
            formated_json = json.loads(json.dumps(getjson))
            _weather_report(formated_json)

        def send_email_out(self):
            """Sends an email from an ESlave object TO all recpients via SMTP_SSL on port 465
            (once account is allowed access under the gmail preferences.)

            """

            print("--> 'Your wish is my command. Sending E-mail out!'")
            server_ssl = smtplib.SMTP_SSL("smtp.gmail.com",465)
            server_ssl.ehlo()
            server_ssl.login(GUSER_NAME, GPASS)
            server_ssl.sendmail(FROM, TO, TESTMESS)
            print("                ~~E-mail sent.~~")

        def send_sms_out(self):
            """Sends a text sms out to a recipient. Uses TwilioRestClient.

            Note: myconfig.get(___,___) pulls values from your myconfig file via
            a SafemyconfigParser named myconfig.

            """

            print "--> 'Your wish is my command. Sending SMS-Texts out!' "
            ACCOUNT_SID = myconfig.get('twilio','ACCOUNT_SID')
            AUTH_TOKEN = myconfig.get('twilio','AUTH_TOKEN')

            twilio_number = myconfig.get('twilio','twilio_number')
            my_cell = myconfig.get('twilio','my_cell')
            body = myconfig.get('twilio','body')

            client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
            client.messages.create(to=my_cell,from_=twilio_number,body=body)
            print "            ~~Text messages sent.~~"



#Helper methods to ESlave()
def _weather_report(jstream):
    """Prints relevant weather information in a pre-arranged order.

    Args:
        jstream = formatted json stream

    """
    print "\nThe temperature in %s on %s is:\n" % (jstream.get('name'), datetime.date.today())
    print "High: %d | Low: %d " % (jstream.get('main').get('temp_max'),jstream.get('main').get('temp_min'))
    print "Rain: '%r' inches" %  jstream.get('rain')
    print "Wind Speed: %s mph\n" % jstream.get('wind').get('speed')

def _gmail_login(connection):
    """Logs into gmail.

    Args:
        connection =  imap connection

    Raises:
        IMAP4.error: for failed login/bad credentials

    """
    try:
        connection.login(GUSER_NAME,GPASS)
        print "~~connection established with {0} ~~".format(GUSER_NAME)
    except imaplib.IMAP4.error:
        print "~~login failed ~~"


def _check_boxes(connection):
    """Checks the available boxes and prints them.

    Args:
        connection =  imap connection

    """
    response, mailboxes = connection.list()
    if response == 'OK':
       print "Mailboxes:"
       print mailboxes

def _open_box(connection, which_box):
    """Selects which box on an email client to perform operations on and opens it.

    Args:
        connection - imap connection
        which_box - which box to perform operations on

    """
    response = connection.select(which_box)
    if response == "OK":
        print "~~Processing selected box~~"

def _process_mailbox(connection):
    """Returns the datetime and and payload for the box

       connection = imap connection

    """
    print "Messages:"
    tr, step = connection.search(None,"ALL")
    if tr != 'OK':
        print "~~No messages found!~~"
        return

    for num in step[0].split():
        tr, step = connection.fetch(num, '(RFC822)')
        if tr != 'OK':
            print "~~ERROR getting message~~", num
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
