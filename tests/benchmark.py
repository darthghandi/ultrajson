﻿# coding=UTF-8
import simplejson
import ultrajson
import sys
try:
    import json
except ImportError:
    json = simplejson
try:
    import yajl
except ImportError:
    yajl = simplejson
from time import time as gettime
import time
import sys
import random


user = { "userId": 3381293, "age": 213, "username": "johndoe", "fullname": u"John Doe the Second", "isAuthorized": True, "liked": 31231.31231202, "approval": 31.1471, "jobs": [ 1, 2 ], "currJob": None }
friends = [ user, user, user, user, user, user, user, user ]

decodeData = ""

"""=========================================================================="""

def ultrajsonEnc():
    x = ultrajson.encode(testObject, ensure_ascii=False)
    #print "ultrajsonEnc", x

def simplejsonEnc():
    x = simplejson.dumps(testObject)
    #print "simplejsonEnc", x

def jsonEnc():
    x = json.dumps(testObject)
    #print "jsonEnc", x

def yajlEnc():
    x = yajl.dumps(testObject)
    #print "yaylEnc", x

"""=========================================================================="""

def ultrajsonEncSorted():
    x = ultrajson.encode(testObject, ensure_ascii=False, sort_keys=True)
    #print "ultrajsonEnc", x

def simplejsonEncSorted():
    x = simplejson.dumps(testObject, sort_keys=True)
    #print "simplejsonEnc", x

def jsonEncSorted():
    x = json.dumps(testObject, sort_keys=True)
    #print "jsonEnc", x

def yajlEncSorted():
    x = yajl.dumps(testObject, sort_keys=True)
    #print "yaylEnc", x

"""=========================================================================="""

def ultrajsonDec():
    x = ultrajson.decode(decodeData)
    #print "ultrajsonDec: ", x

def simplejsonDec():
    x = simplejson.loads(decodeData)
    #print "simplejsonDec: ", x

def jsonDec():
    x = json.loads(decodeData)
    #print "jsonDec: ", x

def yajlDec():
    x = yajl.loads(decodeData)
    #print "yajlDec: ", x

"""=========================================================================="""

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

skip_lib_comparisons = False
if __name__ == "__main__":
    import timeit
    timeit_compat_fix(timeit)
    if len(sys.argv) > 1 and "skip-lib-comps" in sys.argv:
        skip_lib_comparisons = True

print "Array with 256 doubles:"
testObject = []

for x in xrange(256):
    testObject.append(sys.maxint * random.random())
    
COUNT = 10000

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEnc()", "from __main__ import simplejsonEnc", gettime,10, COUNT)), )
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEnc()", "from __main__ import yajlEnc", gettime, 10, COUNT)), )

decodeData = json.dumps(testObject)

print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )
    print "yajl decode       : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlDec()", "from __main__ import yajlDec", gettime,10, COUNT)), )
    
    
print "Array with 256 utf-8 strings:"
testObject = []

for x in xrange(256):
    testObject.append("نظام الحكم سلطاني وراثي في الذكور من ذرية السيد تركي بن سعيد بن سلطان ويشترط فيمن يختار لولاية الحكم من بينهم ان يكون مسلما رشيدا عاقلا ًوابنا شرعيا لابوين عمانيين ")

COUNT = 2000


print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEnc()", "from __main__ import simplejsonEnc", gettime,10, COUNT)), )
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEnc()", "from __main__ import yajlEnc", gettime, 10, COUNT)), )

decodeData = json.dumps(testObject)

print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )
    print "yajl decode       : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlDec()", "from __main__ import yajlDec", gettime,10, COUNT)), )

print "Medium complex object:"
testObject = [ [user, friends],  [user, friends],  [user, friends],  [user, friends],  [user, friends],  [user, friends]]
COUNT = 5000

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEnc()", "from __main__ import simplejsonEnc", gettime,10, COUNT)), )
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEnc()", "from __main__ import yajlEnc", gettime, 10, COUNT)), )

decodeData = json.dumps(testObject)

print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )
    print "yajl decode       : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlDec()", "from __main__ import yajlDec", gettime,10, COUNT)), )

print "Array with 256 strings:"
testObject = []

for x in xrange(256):
    testObject.append("A pretty long string which is in a list")

COUNT = 10000

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEnc()", "from __main__ import yajlEnc", gettime, 10, COUNT)), )

decodeData = json.dumps(testObject)

print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )
    print "yajl decode       : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlDec()", "from __main__ import yajlDec", gettime,10, COUNT)), )


print "Array with 256 True values:"
testObject = []

for x in xrange(256):
    testObject.append(True)

COUNT = 50000

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEnc()", "from __main__ import simplejsonEnc", gettime,10, COUNT)), )
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEnc()", "from __main__ import yajlEnc", gettime, 10, COUNT)), )

decodeData = json.dumps(testObject)

print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )
    print "yajl decode       : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlDec()", "from __main__ import yajlDec", gettime,10, COUNT)), )


print "Array with 256 dict{string, int} pairs:"
testObject = []

for x in xrange(256):
    testObject.append({str(random.random()*20): int(random.random()*1000000)})

COUNT = 5000

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEnc()", "from __main__ import simplejsonEnc", gettime,10, COUNT)), )
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEnc()", "from __main__ import yajlEnc", gettime, 10, COUNT)), )

decodeData = json.dumps(testObject)

print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )
    print "yajl decode       : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlDec()", "from __main__ import yajlDec", gettime,10, COUNT)), )

print "Dict with 256 arrays with 256 dict{string, int} pairs:"
testObject = {}

for y in xrange(256):
    arrays = []
    for x in xrange(256):
        arrays.append({str(random.random()*20): int(random.random()*1000000)})
    testObject[str(random.random()*20)] = arrays

COUNT = 50

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEnc()", "from __main__ import ultrajsonEnc", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEnc()", "from __main__ import simplejsonEnc", gettime,10, COUNT)), )
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEnc()", "from __main__ import yajlEnc", gettime, 10, COUNT)), )

decodeData = json.dumps(testObject)

print "ultrajson decode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonDec()", "from __main__ import ultrajsonDec", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson decode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonDec()", "from __main__ import simplejsonDec", gettime,10, COUNT)), )
    print "yajl decode       : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlDec()", "from __main__ import yajlDec", gettime,10, COUNT)), )

print "Dict with 256 arrays with 256 dict{string, int} pairs, outputting sorted keys:"

print "ultrajson encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("ultrajsonEncSorted()", "from __main__ import ultrajsonEncSorted", gettime,10, COUNT)), )
if not skip_lib_comparisons:
    print "simplejson encode : %.05f calls/sec" % (COUNT / min(timeit.repeat("simplejsonEncSorted()", "from __main__ import simplejsonEncSorted", gettime,10, COUNT)), )
    print "yajl  encode      : %.05f calls/sec" % (COUNT / min(timeit.repeat("yajlEncSorted()", "from __main__ import yajlEncSorted", gettime, 10, COUNT)), )
