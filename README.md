## Introduction

This application encrypts, decrypts, and imports Python variables (often passwords) into the global namespace. It gives you a simple (but secure) way to store private information alongside your regular Python code, and then use that information within a production environment. The code is pure Python, has no third-party dependencies, and (probably) requires no re-coding of your program. Unencrypted secrets never go over the wire, nor touch a production hard drive.

Implementation is as simple as:

    from security import *

## Description

#### Development  

In a development environment, importing security.py will automatically encrypt all of the raw files listed in RAW_FILES, and save an encrypted version of each to disk. I suggest you add _ before each raw file name to indicate insecure information; then add _* to your .gitignore file to automatically exclude those files from your repository.  
  
For example, the application is pre-configured to encrypt _passwords.py (included in this repo for demonstration purposes - do not include the raw password file in your own repo). The file _passwords.py will be encrypted into passwords.py every time you execute your program in your production environment (as defined in DEV_MACHINES).
  
#### Production  
  
In a production environment, importing security.py will automatically decrypt and execute the origianl python file, effectively putting all objects and constants into the global namespace.  

For exqample, if you define python variable constants in _passwords.py, then those variables may then be directly referenced within your code. The module assumes that it is in a production environment unless it is running on a machine listed in DEV_MACHINES. 
  
See hello_world.py for a working example.
  
## Installation

##### Step-by-step instructions to get started

    1. Make a text-based private key. For example:  
    
            kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai  
          
       Save key into the root dir of your development and production machines. For example:  
          
            /key.rc4  
          
       And/or save your key into the Google metadata server (optional - if you use GCE):  
       
            http://metadata.google.internal/computeMetadata/v1/project/attributes/rc4  
    
    2. Copy security.py from GitHub into your project.  

    3. Add the following line of code to your main program:  

          from security import *   

    4. Trick dev UI (at least PyCharm) to provide code completion during development. 
       This does not affect production, as _passwords.py should not exist in production.

            try: from _passwords import *  
            except: pass  

    5. Store private information (such as passwords) as regular python variable assignments  
       in a raw .py file. The default setup assumes you use the file _passwords.py:  

            MYSQL_PASSWORD = MyExample!password4   
            SENDGRID_PWD = THisIS_my44sendgridpwd   
            LOGGLY_URL = 'http://logs-01.loggly.com/inputs/00-00-00-00-00/'   
        
    6. Execute your regular program on your dev machine to encrypt your secret info. The
       import statement (step # 3 above) will auto run security.py and encrypt your info.
       This converts the raw info in _passwords.py into encrypted info in passwords.py
          
    7. Use git to 'push-to-deploy' to production machines. Do NOT include your private
       key in your repo (i.e., exclude the file security.rc4), and do not include your
       raw (unsecure) files in your repo (i.e., exclude the file _passwords.py). 
       
       The files security.rc4 and _passwords.py are included here only as example files.
    
    You are done!    
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with the standard RC4 algorithm. Generate a long, random sequence of ASCII characters and save it into a local file (as defined by the constant KEY_FILE; see the file security.rc4 as an example). You may want to store this file in the root directory, as doing so requires root access; but you may store it in any location you set within KEY_FILE. 

#### Google Compute Engine  
  
This application was initially developed for Google Compute Engine. Store your private key in the Google metadata server (with the private URL defined in METADATA_KEY). This application will automatically (and securely) request your private key from the metadata server. Google automatically enforces access rights and permissions for the metadata server. The advantage of this approach is that you can maintain your private key in just one location (to be used by many GCE instances), and then revoke or change the key with minimal disruption. 
  
#### Disclaimer

I use this code myself on a project for Google Compute Engine and find it works well. I'm posting the code as *_pay-it-forward_* for the many sections of code I use from others. This is NOT a formal application - there is *no support* - there are no guarantees - use it at your own risk. Feel free to fork the repo, improve the code, and push it back.
 
#### Version History

Version 1.0 - January 20, 2015

  * Initial release.
