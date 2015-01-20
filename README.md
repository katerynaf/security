## Overview

This application encrypts, decrypts, and imports Python variables (often passwords) into the global namespace. It gives you a simple (but secure) way to store private information (such as passwords) along with your Python code, and then use that information within a production environment. The code is pure Python and has no third-party dependencies.

    Implementation is as simple as:       from security import *

## Description

In a development environment, importing this module will automatically encrypt all of the raw files listed in RAW_FILES, and save an encrypted version of each file to disk. I suggest you add _ as a prefix before each raw file name (for unencrypted and thus insecure information). Then add _* to your .gitignore file, and git will automatically exclude files starting with _ from your repository. The default configurations refers to the file: _passwords.py

In a production environment, importing this module will automatically decrypt and then import all python code (usually constants) from the original raw .py file (for example, from _passwords.py). The module will import all references into the global namespace, so you may then reference secured variables as you normally would in Python. The module assumes that it is in a production environment unless it is running on a machine listed in DEV_MACHINES. 

Encryption is implemented with the standard RC4 algorithm. You need to provide a file with a long sequence of ASCII characters in it as a private encryption key. You should store your key (your private sequence of ASCII characters) in a local file as defined in KEY_FILE. You may want to store this file in the root directory, as that demonstrates root access to the system (although you may chaneg the location). Alternatively, you may provide access to the key from a restricted server (as defined in KEY_URL). If you provide access to your key by URL, you should (obviously) authenticate and restrict access.  

This application works with Google Compute Engine. Store your private key in the Google metadata server as defined by the METADATA_KEY -- this module will then automatically (and securely) obtain your private key from the metadata server. You can revoke or change the key with minimal downtime. Google automatically enforces access rights and permissions for the metadata server.
  
## Installation & use

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
