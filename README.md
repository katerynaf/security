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

1. Clone this GitHub repo. (Alternatively, you really only need to security.py file and can configure everything else.)

2. Make a private key from ASCII characters. For example:  
    
    `kksdhfs984y5hbswfd8WEZJD8asdhasi!JHADHjasbd78asjdai`  
          
3. Save your private key into a `security.key` file.
    
4. On development machines, the code is pre-configured for you to save `security.key` into the `private/` 
   subdirectory within your current project directory, but you may save it anywhere you wish and then specify the 
   path when you call `security.secure()`  
  
5. On production machines, install the `security.key` file in a **secure location**. Do NOT include the encryption key
   in push-to-deploy configurations or your GitHub repo. Instead, manually install the `security.key` file into a 
   secure location on the production machine(s).  The code is preconfigured to find the `security.key` file in your 
   user home directory, although I tend to override that settings and save my security key in the root directory 
   because that implies root access.  
      
6. Add the following two lines to your main program:  
  
    `import security`  
    `security.secure()`  
  
8. (optional) Trick your development environment to provide code completion (e.g., PyCharm): 
  
    `try: from _private.passwords import *`  
    `except: pass`  
  
    Include error handling in the code above because the original file should NOT exist in your production environment
    and the above import will therefore fail in your production environment. The exact coding above will depend 
    on how/where you store files (the above works for the default configuration).
  
9. Store your secret information as Python variable statements in a standard python file. Do NOT span lines -- this
   is a limitation of the program. With a little work, someone could revise the code to handle multiple lines, but this
   works for my needs (I store all of my secrets as single-lined variables). For example, a passwords.py file might 
   look something like:
         
    `MYSQL_PASSWORD = "MyExample!password4"`  
    `SENDGRID_PWD = "THisIS_my44sendgridpwd"`  
    `LOGGLY_URL = "http://logs-01.loggly.com/inputs/00-00-00-00-00/"`
        
10. Deploy your code (maybe use 'push-to-deploy' and git). Include encrypted files (such as `passwords.rc4`) in your
    deployment, but DO NOT include unencrypted files from the `_private/` directory, nor your `security.key` file, in 
    the deployment. You should deploy the `security.key` file manually as noted in step 4 above. 
    
    I install my `security.key` file in a custom Ubuntu Image that I use on Google Compute Engine; it is then available 
    to all instances. Use the `.gitignore` file to keep private files and your security key out of the GIT repo. 
       
You're done!    
  
  
## Technical notes 
 
#### Encryption
  
Encryption is implemented with a standard RC4 algorithm. Generate a long, random sequence of ASCII characters and 
save it into a local file. This project includes the file `security.rc4` as an example, but you should change it.

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
