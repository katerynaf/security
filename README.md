## Introduction

This application encrypts, decrypts, and imports passwords (and other private information) as Python variables in the
global namespace. It provides a simple and secure way to maintain secrets within regular Python code, and then use 
those secrets in a production environment. The code is pure Python, has no third-party dependencies, and should
require no re-coding of your program. Unencrypted secrets never go over the wire or touch a production hard drive.

Implementing this code is as simple as:  `from security import *`

## Description

#### During development

Including `from security import *` with your program will encrypt every file listed in `FILES` and save each file to
disk with a `*.rc4` extension. For example, this repo is pre-configured to encrypt `passwords.py` into 
`passwords.rc4`. You may include additional files, or other files, by listing them in the `FILES` variable. Files are
encrypted automatically every time the statement `from security import *` is executed (and it can find the original
files), so run your program at least once on your development machine each time you change your private files 
 (suca as `passwords.py`). 
  
#### During production  
  
In a production environment, importing security.py (again, by using `from security import *`) will automatically 
decrypt your python file and place all variable statements from the original file into your global namespace. 
Unencrypted secrets never go over the wire or touch a production hard drive; instead, you can reference those
secrets as regular python variables, directly within your code. See hello_world.py for a working example.
  
## Installation

##### Step-by-step instructions to get started

    1. Make a private key from a string of ASCII characters. For example:  
    
            kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai  
          
    2. Save your ASCII characters into a file to serve as your encryption key. Save that file in a secure location on
       both your development and production machines -- for example, in the root directory:
    
            /security.key  
              
    3. Copy the module `security.py` from GitHub into your project, and then import it into your project with the
       following statement:  

          from security import *    
          
      Yes - DO use the asterisk approach as shown above, in order to import your information into the global namespace.

    4. Trick your development UI (e.g., PyCharm) to provide code completion during development. 

            try: from passwords import *  
            except: pass  

        Include error handling, because the original file should not exist in production environments and the import 
        will therefore fail.

    5. Define your secret information as standard Python variable statements. Do NOT span lines. Each statement must 
       stay on one line. For example, the file passwords.py might include:
         
            MYSQL_PASSWORD = MyExample!password4  
            SENDGRID_PWD = THisIS_my44sendgridpwd  
            LOGGLY_URL = 'http://logs-01.loggly.com/inputs/00-00-00-00-00/' 
        
    6. Deploy your code (perhaps use git to 'push-to-deploy'). Include the encrypted passwords.rc4 file in your 
       deployment (for example), but DO NOT include the original, unencrypted file passwords.py (for example). 
    
    You're done!    
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with the standard RC4 algorithm. Generate a long, random sequence of ASCII characters and 
save it into a local file (as defined by the constant `KEY_FILE`). I have included the file `security.rc4` as an example. 
You may want to store your encryption key in the root directory, as doing so requires root access -- but you may store 
it in any location you specify in `RC4_KEY`. 

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
