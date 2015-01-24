"""Hello world example using the security module"""

from security import *
try: from passwords import *   # trick PyCharm into providing code completion
except: pass
print(HELLO_WORLD)
