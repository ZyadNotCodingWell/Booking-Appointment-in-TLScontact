"""
A simple script to check the available appointment of TLScontact
Copyright (c) 2014 N00d1e5. All Rights Reserved.
"""

#!/usr/bin/python
import requests
import sys
import time

__author__ = "N00d1e5"

# Values to change
email = ''  # E-mail of TLScontact
pwd = ''  # Password of TLScontact
TLS_EDI = 'https://fr.tlscontact.com/gb/EDI/index.php'  # Homepage with location
TLS_CNX = 'https://fr.tlscontact.com/gb/EDI/login.php'  # Connexion page
TLS_APP = 'https://fr.tlscontact.com/gb/EDI/myapp.php'  # Application page
DELAY = 300  # In second
MONTH_WANT = 4  # Type the latest month you want
DAY_WANT = 30  # Type the latest day of the month you want
FORBIDDEN_WORD = 'TLScontact | Security Notice'  # Block notice
APPOINTMENT_GOT = 'Appointment Confirmation with TLScontact'  # Appointment check

s = requests.session()


def main(username, password):
    while (1):
        if (not test_connexion()):
            if reconnect(username, password):
                print("Status: reconnected.")
            else:
                sys.exit("Connection failed.")

        (month, day, hour, minute) = check_appiontement()

        if check_satisfait(month, day, MONTH_WANT, DAY_WANT):
            print(
                "++++++++++++++++++++\n++ GO and get it! ++\n+ %s-%s-%s %s:%s "
                "+\n++++++++++++++++++++" % (month, day, hour, minute))
        else:
            print("Nothing with %s-%s %s:%s" % (month, day, hour, minute))

        time.sleep(DELAY)


# Check if logged in
def test_connexion():
    r = s.get(TLS_APP)
    # if conntected, we could get the application page
    return (r.url != TLS_EDI and check_forbidden(r))


# Check if blocked
def check_forbidden(r):
    return (FORBIDDEN_WORD not in r.text)


# Reconnect in case of disconnection
def reconnect(username, password):
    sid = get_sid()
    return authenticate(username, password, sid)


# Get secure ID
def get_sid():
    req = s.get(TLS_CNX)
    return (req.text.split('var secret_id = "')[1].split('";')[0])


# Log in
def authenticate(username, password, sid):
    payload = {'process': 'login', '_sid': sid, 'email': email, 'pwd': pwd}
    s.post(TLS_CNX, data=payload)
    r = s.get(TLS_APP)
    is_pass = check_forbidden(r)
    if (r.url != TLS_EDI and is_pass):
        return True
    elif (not is_pass):
        sys.exit("Connexion blocked, increse valur DELAY in the code.")
    else:
        sys.exit("Connection failed, please check your information.")


# Find the earliest appointment
def check_appiontement():
    req = s.get(TLS_APP)

    # Are you kidding me
    if (APPOINTMENT_GOT in req.text):
        sys.exit("You have booked an appointment, call TLScontact to cancel.")
    else:
        (date, time) = req.text.split("<a class='dispo")[0].split(
            "overable'>")[-1].split(" <a class='full' type='button'>")[0:]
        (month, day) = date.split('-')[1:]
        time = time.split('</i>')[0]
        (hour, minute) = time.split('<i>:')[0:2]

        # The time got is the one before the first dispo
        # What happened if the first dispo at 08:30, to modify
        if (minute == '30'):
            hour = str(int(hour) + 1).zfill(2)
            minute = '00'
        else:
            minute = '30'
        return (month, day, hour, minute)


# Check if the earliest satisfait you
def check_satisfait(month, day, MONTH_WANT, DAY_WANT):
    return ((month <= MONTH_WANT) and (day <= DAY_WANT))


# If you say so, get it
def get_appointment():
    return 0


# Action
main(email, pwd)