## OVERVIEW

> Module encrypts, decrypts, and imports variables into the global namespace. This provides a simple, but secure, way to store passwords in Python.


## DESCRIPTION:

This module automatically encrypts a file (named in CONFIG_FILE) during development, and decrypts/imports it (i.e., executes it) during production. Module assumes that it is in production, unless it is running on one of the DEV_MACHINES. Importing module on one of the DEV_MACHINES will auto-encrypt the file defined in the CONFIG_FILE into a shadow copy of that file in the current directory of your development machine. Prefix the filename defined in CONFIG_FILE file with a "_" (e.g.: "_settings.py") and add "_*" to your .gitignore file; doing so causes all files starting with "_" to be excluded from your GIT repo. The original (unencrypted) file will NOT appear in your GIT repo (where you do not want it!). All code within your CONFIG_FILE must be executable line-by-line python; do not use statements, expressions, etc. that span multiple lines.  

> Encryption is implemented with the standard RC4 algorithm. You need to make your own, private encryption key as a long sequence of ASCII chars. Store your private key in a file (KEY_FILENAME) or a server (KEY_URL). Save a copy of your private key in the root directory (demonstrating root access). If you provide access to your private key by URL, then you should (obviously) authenticate and restrict access to the URL.  

> This code was developed with Google Compute Engine in mind. You can store your private key in the Google metadata server and define the URL to it in METADATA_KEY. Your entire project then has access to the private key and you can revoke or change the key centrally with minimal downtime. Google automatically enforces access rights and priviledges to the metadata server.
  
  
## REQUIREMENTS:

> Pure Python. No dependencies. Imports os and urllib2, but you may drop urllib2 if you always use a private key file. 

## HOW TO USE:

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
