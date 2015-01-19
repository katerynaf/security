"""Secure system to encrypt, decrypt, import a .py file into global namespace

OVERVIEW
--------

    Module encrypts, decrypts, and imports variables into the global namespace.
    This provides a simple, but secure, way to store passwords in Python.


DESCRIPTION:
------------

    This module automatically encrypts some file (hardcoded as CONFIG_FILE)
    during development, and decrypts/imports it (i.e., executes it) during
    production. Module assumes that it is in production, unless it is running
    on one of the DEV_MACHINES. Importing module on one of the DEV_MACHINES
    will auto-encrypt the file defined in CONFIG_FILE into a shadow copy
    of that file in the current directory of your development machine. Prefix
    filename defined in CONFIG_FILE file with a "_" (e.g.: "_settings.py")
    and add "_*" to your .gitignore file; doing so causes all files starting
    with "_" to be excluded from your GIT repo. The original (unencrypted)
    file will NOT appear in your GIT repo (where you do not want it!).
    All code within your CONFIG_FILE must be executable line-by-line python;
    do not use statements, expressions, etc. that span multiple lines.

    Encryption is implemented with the standard RC4 algorithm. You need to
    make your own, private encryption key as a long sequence of ASCII chars.
    Store your private key in a file (KEY_FILENAME) or a server (KEY_URL).
    Save a copy of your private key in the root directory (demonstrating root
    access). If you provide access to your private key by URL, then you should
    (pretty obviously) authenticate and restrict access to the URL in some way.

    This code was developed with Google Compute Engine in mind. You can store
    your private key in the Google metadata server and define the URL to it
    in METADATA_KEY. Your entire project then has access to the private key
    and you can revoke or change it centrally with minimal downtime. Google
    automatically enforces access and priviledges to the metadata server.


REQUIREMENTS:
-------------

    None. Pure Python. Module imports os and urllib2 but code can be revised
    to drop urllib2 if you always use a local private key file.


HOW TO INSTALL/USE:
-------------------

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
    The above variables never hit the production harddrive or go over the wire.

"""
__module__    = 'security.py'
__author__    = "Kenneth A Younge"
__copyright__ = "Copyright (c) 2014, Kenneth A Younge"
__license__   = "GNU General Public License"
__email__     = "kenyounge@gmail.com"

import os
import urllib2

DEV_MACHINES  =  ['Kens-MacBook-Pro-3.local', ]  # authorized development machines
CONFIG_FILE   =  '_settings.py' # raw file; prefix with _ and add _* to .gitignore
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

# Encrypt variables and values
try:
    if os.uname()[1] in DEV_MACHINES:
        with open(CONFIG_FILE, 'r') as f: txt = f.read()
        txt = crypt(str(txt).strip(), KEY).encode('hex')
        with open(CONFIG_FILE[1:], 'w') as f: f.write(txt)
except Exception as e:
    print 'Unable to encrypt ' + CONFIG_FILE + ': ' + str(e)

# Decrypt and import variables and values
try:
    with open(CONFIG_FILE[1:], 'r') as f:
        txt = crypt(str(f.read()).strip().decode('hex'), KEY)
    for line in txt.splitlines():
        line = str(line).strip()
        if line: exec line in globals()
except Exception as e:
    print 'Unable to import ' + CONFIG_FILE + ': ' + str(e)
