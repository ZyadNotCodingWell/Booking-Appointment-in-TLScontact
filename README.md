# Booking Appointment in TLScontact

**A simple script to check the available appointment of TLScontact.**

Tested with Visa Application Centre for France in Edinburgh and London, the United Kingdom.

## Usage:

```
usage: TLScontact.py [-h] [-d DELAY] [-v] login password month day

Script to check the available appointment of TLScontact.

positional arguments:
  login                      TLScontact login (e-mail address)
  password                   TLScontact password
  country                    The country code of your application center (gb for the UK)
  city                       The city code of your application center (LON for London)
  month                      The latest acceptable month
  day                        The latest acceptable day

optional arguments:
  -h, --help                 show this help message and exit
  -d DELAY, --delay DELAY    delay between attempts, in seconds(default: 300)
  -v, --verbose              verbose mode
```

*The country code and city code could be found in the TLScontact url.*

## To-Do:

* Check if country code and city code legal
* Add booking appointment function (The appointment can't be canceled by ourselves, averse to test)
* Replace sleep with Emmm...

_Coded for 🍳_
