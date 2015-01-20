## Overview

This "security" application encrypts, decrypts, and imports Python variables into the global namespace. It gives you a simple (but secure) way to store passwords and other private information that your Python code needs to use in a production environment. It works through a simple import call. The code is pure Python with no third-party dependencies.

## Description:

Importing this module in a development environment will automatically encrypt all fo the raw files listed in RAW_FILES, and save an encrypted version of each file to disk. I suggest adding the prefix of "_" to each raw (unencrypted) file (for example: "_settings.py"). If you then add "_*" to your .gitignore file, git will leave the unencrypted version of the raw out of your GIT repository. 

Importing this module in a production environment will automatically decrypt and then import all code & variables from the original raw file. It will import all references into the global namespace so you may then reference those variables as you normally would in Python. The module assumes that it is in a production environment unless it is running on a machine listed in the DEV_MACHINES. 

Encryption is implemented with the standard RC4 algorithm. You need to provide a file with a long sequence of ASCII chars in it to serve as your private encryption key. You should store your private key file (as defined in KEY_FILE) in the root directory (demonstrating root access), or you should provide access to the key from a restricted server (as defined in KEY_URL). If you provide access to your key by URL, you should (obviously) authenticate and restrict access.  

This code was developed with Google Compute Engine in mind. You can store your private key in the Google metadata server and define the URL to it in METADATA_KEY. Your entire project will then have access to your private key and you can revoke or change the key centrally, with minimal downtime. Google automatically enforces access rights to the metadata server.
  
  
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
