"""Encrypt, decrypt, and import python variables into the global namespace.

    Copyright (c) 2014, Kenneth A Younge
    See README.md for documentation.
    See LICENSE for terms and conditions.

"""
__module__    = 'security.py'
__author__    = "Kenneth A Younge"
__copyright__ = "Copyright (c) 2014, Kenneth A Younge"
__license__   = "GNU General Public License"
__email__     = "kenyounge@gmail.com"

import os

RC4_KEY = '/security.key'  # filename of private key -- generally stored in root
FILES   = ['passwords.rc4', ] # list of unencrypted files to encrypt

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

for fname in FILES:

    key = open(RC4_KEY, 'r').read()
    rc4name = fname.replace('.py','.rc4')

    # Encrypt 
    try:
        if os.path.exists(fname):
            with open(fname, 'r') as f: txt = f.read()
            txt = crypt(str(txt).strip(), key).encode('hex')
            with open(rc4name, 'w') as f: f.write(txt)
    except Exception as e:
        print 'Unable to encrypt ' + fname + ' into ' + rc4name + '  Error = ' + str(e)

    # Decrypt 
    try:
        with open(rc4name, 'r') as f:
            txt = crypt(str(f.read()).strip().decode('hex'), key)
        for line in txt.splitlines():
            line = str(line).strip()
            if line:
                try:
                    exec line in globals()
                except:
                    print('Warning - you may have a coding error in ' + fname +
                          ' Python code  in ' + fname + ' can NOT span lines!')
    except Exception as e: print str(e)
