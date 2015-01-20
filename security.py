"""Module encrypts, decrypts, and imports python variables into the global namespace.

## Overview

This "security" application encrypts, decrypts, and imports Python variables into the global namespace. It gives you a
simple (but secure) way to store passwords and other private information that your Python code needs to use in a
production environment. It works through a simple import call. The code is pure Python with no third-party dependencies.

## Description:

Importing this module in a development environment will automatically encrypt raw files (as listed in RAW_FILES) and
save an encrypted version of each file to disk. Prefix the name of each raw (unencrypted) file with "_"
(e.g.: "_settings.py"). If you add "_*" to your .gitignore file, then unencrypted files starting with "_" will be
excluded from your GIT repository.

Importing this module in a production environment will automatically decrypt and then import all code & variables from
the original raw file. It will import all references into the global namespace so you may then reference those variables
as you normally would in Python. The module assumes that it is in a production environment unless it is running on a
machine listed in the DEV_MACHINES.

Encryption is implemented with the standard RC4 algorithm. You need to provide a file with a long sequence of ASCII
chars in it to serve as your private encryption key. You should store your private key file (as defined in KEY_FILE)
in the root directory (demonstrating root access), or you should provide access to the key from a restricted server
(as defined in KEY_URL). If you provide access to your key by URL, you should (obviously) authenticate and restrict
access.

This code was developed with Google Compute Engine in mind. You can store your private key in the Google metadata server
and define the URL to it in METADATA_KEY. Your entire project will then have access to your private key and you can
revoke or change the key centrally, with minimal downtime. Google automatically enforces access rights to the metadata
server.


## Installation & use:

    1. Copy this file (security.py) from GitHub into your project directory.

    2. Add the following line of code to your program (will auto-run module):

        from security import *

    3. To trick dev UI programs such as PyCharm into interpreting your raw
       file and providing code completion during development, add these
       lines of code to your main program (change "_settings" to reflect
       the actual module filename you define in CONFIG_FILE):

        try: from _settings import *
        except: pass

    4. Store passwords as python variable statements in _settings.py file:

        MYSQL_PASSWORD = MyExample!password4
        SENDGRID_PWD = THisIS_my44sendgridpwd
        LOGGLY_URL = 'http://logs-01.loggly.com/inputs/00-00-00-00-00/'
        etc...

        During development, the above variables are encrypted and saved in a file.
        In production, the above variables are decrypted/imported into namespace.
        Decrypted variables never go over the wire or hit the production harddrive.

"""
__module__    = 'security.py'
__author__    = "Kenneth A Younge"
__copyright__ = "Copyright (c) 2014, Kenneth A Younge"
__license__   = "GNU General Public License"
__email__     = "kenyounge@gmail.com"

import os
import urllib2

DEV_MACHINES  =  ['Kens-MacBook-Pro-3.local', ]  # authorized development machines
RAW_FILES     =  ['_passwords.py', ] # list of unencrypted files needing encryption
KEY_FILE      =  'patrf.rc4'  # filename of a private key stored in root ( / )
KEY_URL       =  'http://metadata.google.internal/computeMetadata/v1/project/attributes/rc4'

try:     KEY  =  urllib2.urlopen(urllib2.Request( KEY_URL,
                    headers={ 'Metadata-Flavor' : 'Google' })).read()
except:  KEY  =  open('/' + KEY_FILE, 'r').read()

def crypt(data, key):
    x = 0
    box = range(256)
    for i in range(256):
        x = (x + box[i] + ord(key[i % len(key)])) % 256
        box[i], box[x] = box[x], box[i]
    x = 0
    y = 0
    out = []
    for char in data:
        x = (x + 1) % 256
        y = (y + box[x]) % 256
        box[x], box[y] = box[y], box[x]
        out.append(chr(ord(char) ^ box[(box[x] + box[y]) % 256]))
    return ''.join(out)

for rawname in RAW_FILES:

    securename = rawname[1:]  # change if you use a different naming convention

    # Encrypt variables and values
    try:
        if os.uname()[1] in DEV_MACHINES:
            with open(rawname, 'r') as f: txt = f.read()
            txt = crypt(str(txt).strip(), KEY).encode('hex')
            with open(securename, 'w') as f: f.write(txt)
    except Exception as e:
        print 'Unable to encrypt ' + rawname + ': ' + str(e)

    # Decrypt and import variables and values
    try:
        with open(securename, 'r') as f:
            txt = crypt(str(f.read()).strip().decode('hex'), KEY)
        for line in txt.splitlines():
            line = str(line).strip()
            if line:
                try:
                    exec line in globals()
                except:
                    'Warning - you may have a coding error in ' + rawname + '  Code can NOT span lines.'
    except Exception as e:
        print 'Unable to import ' + rawname + ': ' + str(e)
