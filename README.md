## Introduction

This application encrypts, decrypts, and imports Python variables (often passwords) into the global namespace. It gives you a simple (but secure) way to store private information alongside your regular Python code, and then use that information within a production environment. The code is pure Python, has no third-party dependencies, and (probably) requires no re-coding of your program. Unencrypted secrets never go over the wire, nor touch a production hard drive.

Implementation is as simple as:

    from security import *

## Description

#### Development  

In a development environment, importing security.py will automatically encrypt all of the raw files listed in FILES, and save an encrypted version of each (ending in *.rc4) to disk. You should add your secure files listed in FILES to .gitignore so that they are excluded from your repository.  
  
For example, the application is pre-configured to encrypt passwords.py into passwords.rc4. The file passwords.py is included in this github repository for demonstration purposes, but DO NOT include the raw password.py file in your own published repo. The file passwords.py will be encrypted into the file passwords.rc4 every time you execute your program with the `from security import *` in it (and when the raw, unencrypted file is available).
  
#### Production  
  
In a production environment, importing security.py (with a `from security import *` statement) will automatically decrypt your python file and place all variables into the global namespace. For example, if you define python variable constants in passwords.py, then those variables may then be directly referenced within your code. 
  
See hello_world.py for a working example.
  
## Installation

##### Step-by-step instructions to get started

    1. Make a private key as a string of ASCII characters. 
       For example:  
    
            kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai  
          
       Save the ASCII characters into a file in a secure directory on both your development and production machines. 
       For example, you could save it into a file in the root directory (which requires root permission):  
          
            /security.key  
              
    2. Copy the module file security.py from GitHub into your project, and import it into your project.  

          `from security import *`       (import it into your global namespace with the asterisk)

    3. (optional) Trick your development UI (e.g., PyCharm) to provide code completion during development. 

            `try: from _passwords import *`  
            `except: pass`  

        Note that the above should not affect production, as _passwords.py should not exist in production.

    4. Store your private information (such as passwords) as regular python variable assignments in a .py file. 
       For example, the default setup assumes that you are using the raw file passwords.py to hold secrets. Those
       secrets should be executable, Python statements (do NOT span lines) such as:

            MYSQL_PASSWORD = MyExample!password4   
            SENDGRID_PWD = THisIS_my44sendgridpwd   
            LOGGLY_URL = 'http://logs-01.loggly.com/inputs/00-00-00-00-00/'   
        
    6. Executing the ( from security import * ) statement above will automatically encrypt your secret info. 
       For example, running your program with the above will convert the raw _passwords.py into encrypted passwords.py
          
    7. Use git to 'push-to-deploy.' Do NOT include your private key in your repo (i.e., exclude security.rc4).
       Do not include your raw (un-encrypted) files in your repo (i.e., _passwords.py). 
       
       security.rc4 and _passwords.py are included in THIS repo as examples - exclude them from YOUR repo.  
    
    You're done!    
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with the standard RC4 algorithm. Generate a long, random sequence of ASCII characters and save it into a local file (as defined by the constant KEY_FILE; see the file security.rc4 as an example). You may want to store this file in the root directory, as doing so requires root access; but you may store it in any location you specify within KEY_FILE. 

#### Disclaimer

I use this code in a project for Google Compute Engine and find it works well. I'm posting it to *_pay-it-forward_* for the many sections of code I have borrowed from others. This is NOT a formal application, so there is *no support,* no guarantees, and you agree to use it at your own risk. Feel free to fork the repo and improve the code - if you do so, please submit it back!
 
#### Version History

Version 1.01 - January 23, 2015

  * Simplified the code by removing the google metadata server options.

Version 1.0 - January 20, 2015

  * Initial release.
