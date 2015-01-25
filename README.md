## Introduction

This application encrypts, decrypts, and imports passwords (and other private information) as Python variables in the
global namespace. It provides a simple and secure way to maintain secrets within regular Python code, and then use 
those secrets in a production environment. The code is pure Python, has no third-party dependencies, and should
require no re-coding of your program. Unencrypted secrets never go over the wire or touch a production hard drive.

Implementing this code is as simple as:

    `from security import *`

## Description

#### In the development environment

Importing security.py with `from security import *` will cause every file listed in `FILES` to be automatically 
encrypted and saved to disk. For example, the code is pre-configured to encrypt the file `passwords.py` into 
`passwords.rc4`. The file passwords.py is included here for demonstration purposes, but you should NOT include it
in a public repository or in production. Instead, you should distribute the encrypted file (e.g., `passwords.rc4`) 
and seperately install your encryption key (`security.key`) on each production machine. The file `passwords.py` 
will be encrypted into `passwords.rc4` every time the code segment `from security import *` executes in your
main program in your development environment (i.e., when it can access the raw, unencrypted file for `passwords.py`).
  
#### In the production environment  
  
In a production environment, importing security.py (with a `from security import *` statement) will automatically 
decrypt your python file and place all variables into the global namespace. For example, if you define python variable 
constants in passwords.py, then those variables may then be directly referenced within your code. 
See hello_world.py for a working example.
  
## Installation

##### Step-by-step instructions to get started

    1. Make a private key as a string of ASCII characters. For example:  
    
            `kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai`  
          
    2. Save your ASCII characters into a file in a secure directory on both your development and production machines. 
       For example, save it into the root directory (which requires root permission), as so:  
          
            `/security.key`  
              
    2. Copy the file `security.py` from GitHub into your project, and then `import security` into your project.  

          `from security import *`    (you SHOULD use the asterisk to import it into your global namespace)

    3. Trick your development UI (e.g., PyCharm) to provide code completion during development. 

            `try: from passwords import *`  
            `except: pass`  

        Include error handling becuase the actual file will not exist in production environments.

    4. Within `passwords.py` (or other files that you name in FILES), include your secret information as regular 
       variable statements that are executable within python. Do NOT span lines (each statement must stay on one line).

            `MYSQL_PASSWORD = MyExample!password4`   
            `SENDGRID_PWD = THisIS_my44sendgridpwd`   
            `LOGGLY_URL = 'http://logs-01.loggly.com/inputs/00-00-00-00-00/'`   
        
    6. Include the statement `from security import *` as shown above to automatically encrypt your FILES on your
       development machine. You must execute your program at least once on your development machine for this to work.
          
    7. Use git to 'push-to-deploy' your code. Include the passwords.rc4 file in your deployment (for example), but
       DO NOT include the origianl unencrypted file (passwords.py for example). 
    
    You're done!    
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with the standard RC4 algorithm. Generate a long, random sequence of ASCII characters and 
save it into a local file (as defined by the constant KEY_FILE; see the file security.rc4 as an example). You may want 
to store this file in the root directory, as doing so requires root access; but you may store it in any location you 
specify within RC4_KEY. 

#### Disclaimer

I use this code in a project for Google Compute Engine and find it works well. I'm posting it to *_pay-it-forward_* 
for code I have borrowed from others. There is *no support* and *no guarantees* with this code - so 
*use it at your own risk*. Feel free to fork the repo and improve the code!
 
#### Version History

Version 1.01 - January 23, 2015

  * Simplified the code by removing the google metadata server options.

Version 1.0 - January 20, 2015

  * Initial release.
