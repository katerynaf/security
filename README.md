## Introduction

This application encrypts, decrypts, and imports passwords and other secret information. It provides a simple but secure 
way to maintain secret information within regular Python files (`.py` files), and then access that information
by referencing variables in the global namespace. The code is pure Python, has no third-party dependencies, and 
should require almost no re-coding of your program. Unencrypted secrets are never stored on a production hard-drive.

Implementation is as simple as:
  
    import security
    security.secure()
    
    
## Description

#### Development

When you call `import security` and run `security.secure()` in a development environment, the code will automatically 
**encrypt** a list of python files into a secure format with a `*.rc4` extension. By default, the `security.secure()` 
function will encrypt the file `private/passwords.py` within your project directory, and store the encrypted file
`passwords.rc4` in the current project directory. Be sure to execute `import security` and `security.secure()` each time 
you change your private information. When you include the two lines of code shown above in your main program, it will 
automatically re-synchronize your files each time you run your program in your development environment.
  
#### Production  
  
When you call `import security` and run `security.secure()` in a production environment, the code will automatically
**decrypt** and then **import** your original Python file (the raw version) -- placing variables from the original file
into the global namespace. Unencrypted secrets are never stored on a production hard-driveor go over the wire. 
And yet you can reference your secrets from within your code by simply referencing the original Python variables names.  

Please see hello_world.py for a working example. The line `print(HELLO_WORLD)` is demonstrating that the encrypted
variable HELLO_WORLD is now available at runtime. 
  
  
## Installation & Programming

1. Make a private key from ASCII characters. For example:  
    
    `kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai`  
          
2. Save your private key into a file. For example:
    
    `security.key`  
    
3. On development machines, the solution is preconfigured for you to save your security.key into a sub-directory 
       called `private/` within your current project directory, but you may save it anywhere you wish and specify the 
       path in your call to `security.secure()`  
  
4. On production machines, install the security.key file in a secure location. The solution is preconfigured for 
       you to save your security.key in your user home directory, although I tend to save it the root directory because
       that implies root access.  
      
5. Copy the main `security.py` file from GitHub and place it within your project. You may also want to copy the
       _private directory and it's contents to help get you started (but be sure to change the example security.key !)  
  
6. Add the following two lines to your main program:  
  
    `import security`  
    `security.secure()`  
  
8. (optional) Trick your development environment to provide code completion (e.g., you use PyCharm): 
  
    `try: from _private.passwords import *`  
    `except: pass`  
  
Include error handling in the import above because the original file should NOT exist in your production 
environment and thus the import will fail in your production environment. The exact coding of the above depends 
on whether you use a private directory to store your secret files (the above is the default configuration).
  
9. Store your secret information as Python variable statements in a standard python file. Do NOT span lines -- this
is a limitation of the program, although someone could easily revise the code to handle multiple lines with a
little bit of work. For example, your passwords.py file might look something like:
         
    `MYSQL_PASSWORD = "MyExample!password4"`  
    `SENDGRID_PWD = "THisIS_my44sendgridpwd"`  
    `LOGGLY_URL = "http://logs-01.loggly.com/inputs/00-00-00-00-00/"`
        
6. Deploy your code (maybe use 'push-to-deploy' and git). Include the encrypted files (such as passwords.rc4) in 
your deployment, but DO NOT include the original (unencrypted) files in the deployment or in your GIT repo. 
Use the `.gitignore` file to keep the original private files and your security key out of the GIT repo! 
       
You're done!    
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with a standard RC4 algorithm. Generate a long, random sequence of ASCII characters and 
save it into a local file. This project includes the file `security.rc4` as an example, but in general you will NOT want
to store that file in your private directory.

#### Disclaimer

I use this code in a project for Google Compute Engine and it works well for me. I'm posting it here to 
*_pay-it-forward_* for code I have used from others. I provide *no support* and *no guarantees* - 
*USE THIS CODE AT YOUR OWN RISK*. Feel free to fork the GitHub repo and improve the code!
 
#### Version History

Version 1.03 - January 31, 2015

  * Completely restructured code to import silently and then encrypt/decrypt with a call to `security.secure()`.

Version 1.02 - January 24, 2015

  * Changed the names of constants and the involved files to make them more consistent.

Version 1.01 - January 23, 2015

  * Simplified the code by removing the google metadata server options.

Version 1.0 - January 20, 2015

  * Initial release.
