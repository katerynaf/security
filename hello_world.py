"""Hello World example using the security module"""

import security
security.secure()
try: from _private.passwords import *            # trick PyCharm to provide code completion
except: pass

print(HELLO_WORLD)    # HELLO_WORLD is a variable defined in the original passwords.py file
