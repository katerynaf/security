## Introduction

This application encrypts, decrypts, and imports passwords and other secret information. It provides a simple but secure 
way to maintain secret information within regular Python files (`.py` files), and then access that information
by referencing variables in the global namespace. The code is pure Python, has no third-party dependencies, and 
should require almost no re-coding of your program. Unencrypted secrets are never stored on a production hard-drive.

Implementation is as simple as:
  
    import security
    for line in security.secure(): exec line in globals()
    
    
## Description

#### Development

When you call `import security` and run `for line in security.secure(): exec line in globals()` on a development
machine, the code will first automatically **encrypt** a list of python files into a secure `*.rc4` file. By default,
the code encrypts the file `private/passwords.py` (from your project directory) and stores the encrypted file 
`passwords.rc4` into the current project directory. Be sure to execute the above two lines of code each time you change 
your private information (that should happen automatically when you run your program on your development machine).
  
#### Production  
  
When you call `import security` and run `for line in security.secure(): exec line in globals()` on a production machine, 
the code will automatically **decrypt** and return the original Python statments from your original Python file. The 
code above then executes each line of that code in the calling global environment, so you may then reference the 
original Python variables names as you normally would.

Please see hello_world.py for a working example. The line `print(HELLO_WORLD)` is demonstrating that the original Python
variable `HELLO_WORLD` is now available as a global variable at runtime. 
  
  
## Installation & Programming

1. Clone this GitHub repo (or grab `security.py` and re-configure everything else).

2. Make a private key out of ASCII characters. For example:  
    
    `kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai`  
          
3. Save your private key into the file: `security.key`  
    
4. The code is pre-configured for development machines to access `security.key` from the `private/` subdirectory of
   your current project directory, but you may save it anywhere you wish and specify the path when you call 
   `security.secure()`  
  
5. On production machines, install the `security.key` file in a secure location on the production machine.
   Do NOT include the encryption key in your push-to-deploy sets or GitHub repo. Instead, install the `security.key` 
   file into a **secure location** on the production machines.  The code is pre-configured to find the `security.key` 
   file in the user home directory, although I override that setting and save my security key in the root directory, as 
   that requires root access (but you may not have access to root). 
      
6. Add the following two lines of code to your program:  
  
    `import security`
    `for line in security.secure(): exec line in globals()`
  
8. (optional) Trick your development environment to provide code completion (e.g., PyCharm): 
  
    `try: from _private.passwords import *`  
    `except: pass`  
  
    Include error handling in the code above because `_private.passwords` should NOT exist on your production machine
    and the import will therefore fail. You may change the setting of `_private/` when you call `security.secure()`
  
9. Store your secrets as standard Python variable statements in one or more Python files. Do NOT span lines in your
   variable statements. This is a limitation of the program, although someone could revise the code to handle multiple 
   lines with a little bit of work. A `passwords.py` file. for example, might look something like:
         
    `MYSQL_PASSWORD = "MyExample!password4"`  
    `SENDGRID_PWD = "THisIS_my44sendgridpwd"`  
    `LOGGLY_URL = "http://logs-01.loggly.com/inputs/00-00-00-00-00/"`
        
10. Deploy your code. Include encrypted files such as `passwords.rc4` in your deployment, but **do not** include 
    unencrypted files from the `_private/` directory, or your `security.key` file, in the deployment. 
    
11. Deploy the `security.key` file manually as noted in step 4 above. I install my `security.key` file in a custom 
    Ubuntu Image that I use on Google Compute Engine - it then is available to every instance that I start, and I figure
    that if someone can hack the central Google repository of images, we are all doomed. 
     
12. Add your `_private/` directory to `.gitignore` file to keep private files and your security key out of the GIT repo. 
       
    **That's the 12-step plan - you're done!**      
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with a standard RC4 algorithm. Although RC4 is not as secure as AES, it is simple and fast.
There are rumors that the NSA has broken RC4, but my understanding of RC4 vulnerabilities is that they derive from 
'man-in-the-middle' attacks with large volumes of traffic, or other access to millions of encrypted files needed for
cracking through a statistical analysis. This code presumes that your secrets will change and move over the wire 
infrequently (i.e., a few times, not the millions of times that would be required for a hack); it also assums that you
are encrypting only a handful of files (i.e., not the millions of files that would be required for a statistical 
attack). The advantage of using the "alleged" RC4 algorithm (ARC4) is that you can direclty inspect the code and 
confirm that it is the industry standard. Switching another algorithm such as AES would probably require you to
install another module (such as pycrypto - https://pypi.python.org/pypi/pycrypto), and that involves security risks 
of it's own and a more complicated distribution. 


Please note that you should NOT use the `security.rc4` file included in this repo - that is for demonstration. You 
should generate your own, unique, long, random sequence of ASCII characters and save it into your own 
`security.rc4` file.

#### Disclaimer

I use this code in a project for Google Compute Engine and it works well for me. I'm posting it here to 
*_pay-it-forward_* for code I have used from others. I provide *no support* and *no guarantees* - 
*USE THIS CODE AT YOUR OWN RISK*. Feel free to fork the GitHub repo and improve the code!
 
#### Version History

Version 1.03 - January 31, 2015

  * Completely restructured code to import silently and then encrypt/decrypt with a call to `security.secure()`.

Version 1.0 - January 20, 2015

  * Initial release.
