"""Encrypt, decrypt, and import python variables into the global namespace.

See README.md for documentation. See LICENSE for terms.
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
KEY_FILE      =  '/security.rc4'  # filename of private key -- generally stored in root
KEY_URL       =  'http://metadata.google.internal/computeMetadata/v1/project/attributes/rc4'

try:     KEY  =  urllib2.urlopen(urllib2.Request( KEY_URL,
                    headers={ 'Metadata-Flavor' : 'Google' })).read()
except:  KEY  =  open(KEY_FILE, 'r').read()

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
                try: exec line in globals()
                except: 'Warning - you may have a coding error in ' + rawname + '  Note that code can NOT span lines.'
    except Exception as e:
        print 'Unable to import ' + rawname + ': ' + str(e)
