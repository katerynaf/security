## Overview

This application encrypts, decrypts, and imports Python variables (often passwords) into the global namespace. It gives you a simple (but secure) way to store private information alongside your Python code, and then use that information within a production environment. The code is pure Python, has no third-party dependencies, and requires almost no recoding of your program. Unencrypted secrets never go over the wire or touch a production hard drive.

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
  
## Step-by-Step Instructions

    1. Make a private key, such as:  
    
            kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai  
          
       Save your key into a file in the root directory, such as:  
          
            /key.rc4  
          
       Save your private sequence of characters into the Google metadata server (optional):  
       
            http://metadata.google.internal/computeMetadata/v1/project/attributes/rc4  
    
    2. Copy this file (security.py) from GitHub into your project.  

    3. Add the following line of code to your program:  

          from security import *   

    4. Trick developer programs (such as PyCharm) to provide code completion, by adding   
       the following lines of code to your main program. This does not effect production
       execution, as the _passwords.py file should not exist in production:  

            try: from _passwords import *  
            except: pass  

    5. Store your passwords and private information as regular python variable statements  
       in a raw python .py file, such as _passwords.py. For example:  

            MYSQL_PASSWORD = MyExample!password4   
            SENDGRID_PWD = THisIS_my44sendgridpwd   
            LOGGLY_URL = 'http://logs-01.loggly.com/inputs/00-00-00-00-00/'   
        
    6. Excute your code at least once in your development environment. The line of code
    from step #3 ( from security import * ) will automatically encrypt your secret info.  
          
    7. Use git 'push-to-deploy' into your production environments, excluding secret files.
    
    You're done!  Provide feedback or contribute to the project at GitHub.com  
  
  
## Technical notes 
 
#### Important!
  
    A private key file (security.rc4) and raw password file (_passwords.py) are included in this
    repository for demonstration purposes only. Do NOT include those files in your own repo. 
  
#### Encryption
  
Encryption is implemented with the standard RC4 algorithm. Generate a long, random sequence of ASCII characters and save it into a local file (as defined by the constant KEY_FILE; see the file security.rc4 as an example). You may want to store this file in the root directory, as doing so requires root access; but you may store it in any location you set within KEY_FILE. 

#### Google Compute Engine  
  
This application was initially developed for Google Compute Engine. Store your private key in the Google metadata server (with the private URL defined in METADATA_KEY). This application will automatically (and securely) request your private key from the metadata server. Google automatically enforces access rights and permissions for the metadata server. The advantage of this approach is that you can maintain your private key in just one location (to be used by many GCE instances), and then revoke or change the key with minimal disruption. 
  
#### Disclaimer

I use this code myself for a Google COmpute project. I've released it as a 'pay-it-forward' for the many sections of code I borrow from others. It is NOT a formal application - there is no support - there are no guarantees - use it at your own risk. Feel free to fork the repo, improve the code, and submit it back.
 
