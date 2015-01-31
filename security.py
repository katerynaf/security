"""Secure python variables by encrypting, decrypting, and importing them into the global namespace."""
__module__ = 'security.py'
__author__ = "Kenneth A Younge"
__copyright__ = "Copyright (c) 2014, Kenneth A. Younge"
__license__ = "GNU General Public License"
__email__ = "kenyounge@gmail.com"

import os


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


def secure(file_names=('passwords.py',), key_name='security.key', key_path='~/', pvt_path='_private/', verbose=False):
    """Transform files (encrypt and/or decrypt _private files).

    Keyword arguments:
        filenames  --  sequence of file names to encrypt/decrypt
        key_name   --  file name of your personal rc4 encryption key
        key_path   --  location of encryption key on production machines
        pvt_path   --  location of private files and encryption key during development
        verbose    --   print info

    Defaults:
        filenames  --  passwords.py         a tuple with just one file
        key_name   --  security.key
        key_path   --  ~/                   the user home directory; change to root '/' for tighter security
        pvt_path   --  _private/
        verbose    --  False
    """

    # Load key     (try production location first, otherwise the private directory during development)
    if os.path.exists(os.path.join(key_path, key_name)):
        key = open(os.path.join(key_path, key_name), 'r').read()
    else:
        key = open(os.path.join(os.path.dirname(__file__), pvt_path + key_name), 'r').read()

    # secure each file
    for filename in file_names:

        filename_raw = os.path.join(os.path.dirname(__file__), pvt_path + filename)
        filename_rc4 = os.path.join(os.path.dirname(__file__), os.path.basename(filename).replace('.py', '.rc4'))

        # Encrypt
        try:
            if os.path.exists(filename_raw):
                with open(filename_raw, 'r') as f:
                    text = f.read()
                with open(filename_rc4, 'w') as f:
                    f.write(crypt(str(text).strip(), key).encode('hex'))
                if verbose:
                    print 'Encrypted ' + filename_raw
            else:
                print('File (' + filename_raw + ') not found')
        except Exception as e:
            print(str(e))

        # Decrypt
        try:
            if os.path.exists(filename_rc4):
                with open(filename_rc4, 'r') as f:
                    text = crypt(str(f.read()).strip().decode('hex'), key)
                    for line in [str(line).strip() for line in text.splitlines()]:
                        try:
                            exec line in globals()
                        except Exception as e:
                            print(str(e))
                if verbose:
                    print 'Imported ' + filename_rc4
            else:
                print('File ' + filename_rc4 + ' not found')
        except Exception as e:
            print(str(e))
