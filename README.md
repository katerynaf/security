## Introduction

This application encrypts, decrypts, and imports passwords (and other private information) as Python variables in the
global namespace. It provides a simple and secure way to maintain secrets within regular Python code, and then use 
those secrets in a production environment. The code is pure Python, has no third-party dependencies, and should
require no re-coding of your program. Unencrypted secrets never go over the wire or touch a production hard drive.

Implementing this code is as simple as:

    `from security import *`

## Description

#### During development

Importing security.py (by using `from security import *`) will cause every file listed in `FILES` to be automatically 
encrypted and saved to disk. For example, the code is pre-configured to encrypt the file `passwords.py` into 
`passwords.rc4`. The file `passwords.py` is included in this repo as an example, but you should NOT include it
in a public repository or in production. Instead, distribute the encrypted file `passwords.rc4` with your application
and separately install your encryption key (`security.key`) on each production machine.  
  
The file `passwords.py` is encrypted into `passwords.rc4` every time the code segment `from security import *` is 
executed in your main program in your development environment (i.e., when it can access `passwords.py`), so be sure to 
run your program at least once on your development machine after you make changes in `passwords.py`. You may include
additional files, or other files, by listing them in the `FILES` variable in `security.py`.
  
#### During production  
  
In a production environment, importing security.py (with a `from security import *` statement) will automatically 
decrypt your python file and place all variables into the global namespace. For example, if you define python variable 
constants in passwords.py, then those variables may then be directly referenced within your code. 
See hello_world.py for a working example.
  
## Installation

##### Step-by-step instructions to get started

    1. Make a private key as a string of ASCII characters. For example:  
    
            kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai  
          
    2. Save your ASCII characters into a file in a secure directory on both your development and production machines. 
       For example, save it into the root directory (which requires root permission), as so:  
          
            /security.key  
              
    3. Copy the file `security.py` from GitHub into your project, and then `import security` into your project.  

          from security import *    
          
      You *should* use the asterisk above in order to import the information into your global namespace.

    4. Trick your development UI (e.g., PyCharm) to provide code completion during development. 

            try: from passwords import *  
            except: pass  

        Include error handling because the actual file will not exist in production environments.

    5. Within passwords.py (or other files you name in FILES), include your secret information as regular variable
       statements that are executable within Python. Do NOT span lines (each statement must stay on one line).
       For example:  
         
            MYSQL_PASSWORD = MyExample!password4  
            SENDGRID_PWD = THisIS_my44sendgridpwd  
            LOGGLY_URL = 'http://logs-01.loggly.com/inputs/00-00-00-00-00/' 
        
    6. Use git to 'push-to-deploy' your code. Include the passwords.rc4 file in your deployment (for example), but
       DO NOT include the origianl unencrypted file (passwords.py for example). 
    
    You're done!    
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with the standard RC4 algorithm. Generate a long, random sequence of ASCII characters and 
save it into a local file (as defined by the constant KEY_FILE; see the file security.rc4 as an example). You may want 
to store this file in the root directory, as doing so requires root access; but you may store it in any location you 
specify within RC4_KEY. 

#### Disclaimer

I use this code in a project for Google Compute Engine and it works well for me. I'm posting it here to 
*_pay-it-forward_* for code I have borrowed from others. There is *no support* and *no guarantees* with this code - so 
*use it at your own risk*. Feel free to fork the repo and improve it!
 
#### Version History

Version 1.02 - January 24, 2015

  * Changed the names of constants and the involved files to make them more consistent.

Version 1.01 - January 23, 2015

  * Simplified the code by removing the google metadata server options.

Version 1.0 - January 20, 2015

  * Initial release.
