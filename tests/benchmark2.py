# coding=UTF-8
import simplejson
import ultrajson
import sys
try:
    import json
except ImportError:
    json = simplejson
import cjson
from time import time as gettime
import time
import sys
import random

def timeit_compat_fix(timeit):
    if sys.version_info[:2] >=  (2,6):
        return
    default_number = 1000000
    default_repeat = 3
    if sys.platform == "win32":
        # On Windows, the best timer is time.clock()
        default_timer = time.clock
    else:
        # On most other platforms the best timer is time.time()
        default_timer = time.time
    def repeat(stmt="pass", setup="pass", timer=default_timer,
       repeat=default_repeat, number=default_number):
        """Convenience function to create Timer object and call repeat method."""
        return timeit.Timer(stmt, setup, timer).repeat(repeat, number)
    timeit.repeat = repeat

def ultrajsonDec():
    x = ultrajson.loads(decodeData)

def simplejsonDec():
    x = simplejson.loads(decodeData)
    
def ultrajsonEnc():
    x = ultrajson.dumps(encodeData)

def simplejsonEnc():
    x = simplejson.dumps(encodeData)
        
    
if __name__ == "__main__":
    import timeit
    timeit_compat_fix(timeit)
    
COUNT = 100

# Load file into memory
f = open("sample.json", "rb")
decodeData = f.read()
f.close()

encodeData = simplejson.loads(decodeData)

# Decode 1 million times
print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEnc()", "from __main__ import simplejsonEnc", gettime,10, COUNT)), )

