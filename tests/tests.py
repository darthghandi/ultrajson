﻿
try:
    import unittest2 as unittest
except ImportError:
    import unittest

import ultrajson
try:
    import json
except ImportError:
    import simplejson as json
import math
import platform
import sys
import time
import datetime
import calendar

try:
    from io import StringIO
except:
    from io import StringIO

import re
import random
import decimal
from functools import partial

PY3 = (sys.version_info[0] >= 3)
if PY3:
    xrange = range

def _python_ver(skip_major, skip_minor=None):
    major, minor = sys.version_info[:2]
    return major == skip_major and (skip_minor is None or minor == skip_minor)

json_unicode = (json.dumps if sys.version_info[0] >= 3
                else partial(json.dumps, encoding="utf-8"))

class UltraJSONTests(unittest.TestCase):

    def test_encodeDecimal(self):
        sut = decimal.Decimal("1337.1337")
        encoded = ultrajson.encode(sut, double_precision=100)
        decoded = ultrajson.decode(encoded)
        self.assertEqual(decoded, 1337.1337)

    def test_encodeStringConversion(self):
        input = "A string \\ / \b \f \n \r \t </script> &"
        not_html_encoded = '"A string \\\\ \\/ \\b \\f \\n \\r \\t <\\/script> &"'
        html_encoded = '"A string \\\\ \\/ \\b \\f \\n \\r \\t \\u003c\\/script\\u003e \\u0026"'
        not_slashes_escaped = input

        def helper(expected_output, **encode_kwargs):
            output = ultrajson.encode(input, **encode_kwargs)
            self.assertEqual(input, json.loads(output))
            self.assertEqual(output, expected_output)
            self.assertEqual(input, ultrajson.decode(output))

        # Default behavior assumes encode_html_chars=False.
        helper(not_html_encoded, ensure_ascii=True)
        helper(not_html_encoded, ensure_ascii=False)

        # Make sure explicit encode_html_chars=False works.
        helper(not_html_encoded, ensure_ascii=True, encode_html_chars=False)
        helper(not_html_encoded, ensure_ascii=False, encode_html_chars=False)

        # Make sure explicit encode_html_chars=True does the encoding.
        helper(html_encoded, ensure_ascii=True, encode_html_chars=True)
        helper(html_encoded, ensure_ascii=False, encode_html_chars=True)

        # Do escape forward slashes if disabled.
        helper(not_slashes_escaped, escape_forward_slashes=False)

    def testWriteEscapedString(self):
        self.assertEqual('"\\u003cimg src=\'\\u0026amp;\'\\/\\u003e"', ultrajson.dumps("<img src='&amp;'/>", encode_html_chars=True))

    def test_doubleLongIssue(self):
        sut = {'a': -4342969734183514}
        encoded = json.dumps(sut)
        decoded = json.loads(encoded)
        self.assertEqual(sut, decoded)
        encoded = ultrajson.encode(sut, double_precision=100)
        decoded = ultrajson.decode(encoded)
        self.assertEqual(sut, decoded)

    def test_doubleLongDecimalIssue(self):
        sut = {'a': -12345678901234.56789012}
        encoded = json.dumps(sut)
        decoded = json.loads(encoded)
        self.assertEqual(sut, decoded)
        encoded = ultrajson.encode(sut, double_precision=100)
        decoded = ultrajson.decode(encoded)
        self.assertEqual(sut, decoded)

    def test_encodeDecodeLongDecimal(self):
        sut = {'a': -528656961.4399388}
        encoded = ultrajson.dumps(sut, double_precision=15)
        ultrajson.decode(encoded)

    def test_decimalDecodeTest(self):
        sut = {'a': 4.56}
        encoded = ultrajson.encode(sut)
        decoded = ultrajson.decode(encoded)
        self.assertNotEqual(sut, decoded)

    def test_decimalDecodeTestPrecise(self):
        sut = {'a': 4.56}
        encoded = ultrajson.encode(sut)
        decoded = ultrajson.decode(encoded, precise_float=True)
        self.assertEqual(sut, decoded)

    def test_encodeDictWithUnicodeKeys(self):
        input = { "key1": "value1", "key1": "value1", "key1": "value1", "key1": "value1", "key1": "value1", "key1": "value1" }
        output = ultrajson.encode(input)

        input = { "بن": "value1", "بن": "value1", "بن": "value1", "بن": "value1", "بن": "value1", "بن": "value1", "بن": "value1" }
        output = ultrajson.encode(input)

    def test_encodeDoubleConversion(self):
        input = math.pi
        output = ultrajson.encode(input)
        self.assertEqual(round(input, 5), round(json.loads(output), 5))
        self.assertEqual(round(input, 5), round(ultrajson.decode(output), 5))

    def test_encodeWithDecimal(self):
        input = 1.0
        output = ultrajson.encode(input)
        self.assertEqual(output, "1.0")

    def test_encodeDoubleNegConversion(self):
        input = -math.pi
        output = ultrajson.encode(input)

        self.assertEqual(round(input, 5), round(json.loads(output), 5))
        self.assertEqual(round(input, 5), round(ultrajson.decode(output), 5))

    def test_encodeArrayOfNestedArrays(self):
        input = [[[[]]]] * 20
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        #self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeArrayOfDoubles(self):
        input = [ 31337.31337, 31337.31337, 31337.31337, 31337.31337] * 10
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        #self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_doublePrecisionTest(self):
        input = 30.012345678901234
        output = ultrajson.encode(input, double_precision = 15)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(input, ultrajson.decode(output))

        output = ultrajson.encode(input, double_precision = 9)
        self.assertEqual(round(input, 9), json.loads(output))
        self.assertEqual(round(input, 9), ultrajson.decode(output))

        output = ultrajson.encode(input, double_precision = 3)
        self.assertEqual(round(input, 3), json.loads(output))
        self.assertEqual(round(input, 3), ultrajson.decode(output))

    def test_invalidDoublePrecision(self):
        input = 30.12345678901234567890
        output = ultrajson.encode(input, double_precision = 20)
        # should snap to the max, which is 15
        self.assertEqual(round(input, 15), json.loads(output))
        self.assertEqual(round(input, 15), ultrajson.decode(output))

        output = ultrajson.encode(input, double_precision = -1)
        # also should snap to the max, which is 15
        self.assertEqual(round(input, 15), json.loads(output))
        self.assertEqual(round(input, 15), ultrajson.decode(output))

        # will throw typeError
        self.assertRaises(TypeError, ultrajson.encode, input, double_precision = '9')
        # will throw typeError
        self.assertRaises(TypeError, ultrajson.encode, input, double_precision = None)

    def test_encodeStringConversion(self):
        input = "A string \\ / \b \f \n \r \t"
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, '"A string \\\\ \\/ \\b \\f \\n \\r \\t"')
        self.assertEqual(input, ultrajson.decode(output))

    def test_decodeUnicodeConversion(self):
        pass

    def test_encodeUnicodeConversion1(self):
        input = "Räksmörgås اسامة بن محمد بن عوض بن لادن"
        enc = ultrajson.encode(input)
        dec = ultrajson.decode(enc)
        self.assertEqual(enc, json_unicode(input))
        self.assertEqual(dec, json.loads(enc))

    def test_encodeControlEscaping(self):
        input = "\x19"
        enc = ultrajson.encode(input)
        dec = ultrajson.decode(enc)
        self.assertEqual(input, dec)
        self.assertEqual(enc, json_unicode(input))

    def test_encodeUnicodeConversion2(self):
        input = "\xe6\x97\xa5\xd1\x88"
        enc = ultrajson.encode(input)
        dec = ultrajson.decode(enc)
        self.assertEqual(enc, json_unicode(input))
        self.assertEqual(dec, json.loads(enc))

    def test_encodeUnicodeSurrogatePair(self):
        input = "\xf0\x90\x8d\x86"
        enc = ultrajson.encode(input)
        dec = ultrajson.decode(enc)

        self.assertEqual(enc, json_unicode(input))
        self.assertEqual(dec, json.loads(enc))

    def test_encodeUnicode4BytesUTF8(self):
        input = "\xf0\x91\x80\xb0TRAILINGNORMAL"
        enc = ultrajson.encode(input)
        dec = ultrajson.decode(enc)

        self.assertEqual(enc, json_unicode(input))
        self.assertEqual(dec, json.loads(enc))

    def test_encodeUnicode4BytesUTF8Highest(self):
        input = "\xf3\xbf\xbf\xbfTRAILINGNORMAL"
        enc = ultrajson.encode(input)
        dec = ultrajson.decode(enc)

        self.assertEqual(enc, json_unicode(input))
        self.assertEqual(dec, json.loads(enc))

    # Characters outside of Basic Multilingual Plane(larger than
    # 16 bits) are represented as \UXXXXXXXX in python but should be encoded
    # as \uXXXX\uXXXX in json.
    def testEncodeUnicodeBMP(self):
        s = '\U0001f42e\U0001f42e\U0001F42D\U0001F42D' # 🐮🐮🐭🐭
        encoded = ultrajson.dumps(s)
        encoded_json = json.dumps(s)
		
        if len(s) == 4:
            self.assertEqual(len(encoded), len(s) * 12 + 2)
        else:
            self.assertEqual(len(encoded), len(s) * 6 + 2) 
          
        self.assertEqual(encoded, encoded_json)
        decoded = ultrajson.loads(encoded)
        self.assertEqual(s, decoded)

        # ultrajson outputs an UTF-8 encoded str object
        if PY3:
            encoded = ultrajson.dumps(s, ensure_ascii=False)
        else:
            encoded = ultrajson.dumps(s, ensure_ascii=False).decode("utf-8")

        # json outputs an unicode object
        encoded_json = json.dumps(s, ensure_ascii=False)
        self.assertEqual(len(encoded), len(s) + 2) # original length + quotes
        self.assertEqual(encoded, encoded_json)
        decoded = ultrajson.loads(encoded)
        self.assertEqual(s, decoded)

    def testEncodeSymbols(self):
        s = '\u273f\u2661\u273f' # ✿♡✿
        encoded = ultrajson.dumps(s)
        encoded_json = json.dumps(s)
        self.assertEqual(len(encoded), len(s) * 6 + 2) # 6 characters + quotes
        self.assertEqual(encoded, encoded_json)
        decoded = ultrajson.loads(encoded)
        self.assertEqual(s, decoded)

        # ultrajson outputs an UTF-8 encoded str object
        if PY3:
            encoded = ultrajson.dumps(s, ensure_ascii=False)
        else:
            encoded = ultrajson.dumps(s, ensure_ascii=False).decode("utf-8")

        # json outputs an unicode object
        encoded_json = json.dumps(s, ensure_ascii=False)
        self.assertEqual(len(encoded), len(s) + 2) # original length + quotes
        self.assertEqual(encoded, encoded_json)
        decoded = ultrajson.loads(encoded)
        self.assertEqual(s, decoded)

    def test_encodeArrayInArray(self):
        input = [[[[]]]]
        output = ultrajson.encode(input)

        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeIntConversion(self):
        input = 31337
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeIntNegConversion(self):
        input = -31337
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeLongNegConversion(self):
        input = -9223372036854775808
        output = ultrajson.encode(input)

        outputjson = json.loads(output)
        outputultrajson = ultrajson.decode(output)

        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeListConversion(self):
        input = [ 1, 2, 3, 4 ]
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeDictConversion(self):
        input = { "k1": 1, "k2":  2, "k3": 3, "k4": 4 }
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(input, ultrajson.decode(output))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeNoneConversion(self):
        input = None
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeTrueConversion(self):
        input = True
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeFalseConversion(self):
        input = False
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeDatetimeConversion(self):
        ts = time.time()
        input = datetime.datetime.fromtimestamp(ts)
        output = ultrajson.encode(input)
        expected = calendar.timegm(input.utctimetuple())
        self.assertEqual(int(expected), json.loads(output))
        self.assertEqual(int(expected), ultrajson.decode(output))

    def test_encodeDateConversion(self):
        ts = time.time()
        input = datetime.date.fromtimestamp(ts)

        output = ultrajson.encode(input)
        tup = ( input.year, input.month, input.day, 0, 0, 0 )

        expected = calendar.timegm(tup)
        self.assertEqual(int(expected), json.loads(output))
        self.assertEqual(int(expected), ultrajson.decode(output))

    def test_encodeToUTF8(self):
        input = "\xe6\x97\xa5\xd1\x88"
        enc = ultrajson.encode(input, ensure_ascii=False)
        dec = ultrajson.decode(enc)
        self.assertEqual(enc, json_unicode(input, ensure_ascii=False))
        self.assertEqual(dec, json.loads(enc))

    def test_decodeFromUnicode(self):
        input = "{\"obj\": 31337}"
        dec1 = ultrajson.decode(input)
        dec2 = ultrajson.decode(str(input))
        self.assertEqual(dec1, dec2)

    def test_encodeRecursionMax(self):
        # 8 is the max recursion depth

        class O2:
            member = 0
            pass

        class O1:
            member = 0
            pass

        input = O1()
        input.member = O2()
        input.member.member = input

        try:
            output = ultrajson.encode(input)
            assert False, "Expected overflow exception"
        except(OverflowError):
            pass

    def test_encodeDoubleNan(self):
        input = float('nan')
        try:
            ultrajson.encode(input)
            assert False, "Expected exception!"
        except(OverflowError):
            return
        assert False, "Wrong exception"

    def test_encodeDoubleInf(self):
        input = float('inf')
        try:
            ultrajson.encode(input)
            assert False, "Expected exception!"
        except(OverflowError):
            return
        assert False, "Wrong exception"

    def test_encodeDoubleNegInf(self):
        input = -float('inf')
        try:
            ultrajson.encode(input)
            assert False, "Expected exception!"
        except(OverflowError):
            return
        assert False, "Wrong exception"


    def test_decodeJibberish(self):
        input = "fdsa sda v9sa fdsa"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeBrokenArrayStart(self):
        input = "["
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeBrokenObjectStart(self):
        input = "{"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeBrokenArrayEnd(self):
        input = "]"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeArrayDepthTooBig(self):
        input = '[' * (1024 * 1024)
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeBrokenObjectEnd(self):
        input = "}"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeObjectDepthTooBig(self):
        input = '{' * (1024 * 1024)
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeStringUnterminated(self):
        input = "\"TESTING"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeStringUntermEscapeSequence(self):
        input = "\"TESTING\\\""
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeStringBadEscape(self):
        input = "\"TESTING\\\""
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeTrueBroken(self):
        input = "tru"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeFalseBroken(self):
        input = "fa"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"

    def test_decodeNullBroken(self):
        input = "n"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return
        assert False, "Wrong exception"


    def test_decodeBrokenDictKeyTypeLeakTest(self):
        input = '{{1337:""}}'
        for x in range(1000):
            try:
                ultrajson.decode(input)
                assert False, "Expected exception!"
            except(ValueError) as e:
                continue

            assert False, "Wrong exception"

    def test_decodeBrokenDictLeakTest(self):
        input = '{{"key":"}'
        for x in range(1000):
            try:
                ultrajson.decode(input)
                assert False, "Expected exception!"
            except(ValueError):
                continue

            assert False, "Wrong exception"

    def test_decodeBrokenListLeakTest(self):
        input = '[[[true'
        for x in range(1000):
            try:
                ultrajson.decode(input)
                assert False, "Expected exception!"
            except(ValueError):
                continue

            assert False, "Wrong exception"

    def test_decodeDictWithNoKey(self):
        input = "{{{{31337}}}}"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return

        assert False, "Wrong exception"

    def test_decodeDictWithNoColonOrValue(self):
        input = "{{{{\"key\"}}}}"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return

        assert False, "Wrong exception"

    def test_decodeDictWithNoValue(self):
        input = "{{{{\"key\":}}}}"
        try:
            ultrajson.decode(input)
            assert False, "Expected exception!"
        except(ValueError):
            return

        assert False, "Wrong exception"

    def test_decodeNumericIntPos(self):
        input = "31337"
        self.assertEqual (31337, ultrajson.decode(input))

    def test_decodeNumericIntNeg(self):
        input = "-31337"
        self.assertEqual (-31337, ultrajson.decode(input))

    def test_encodeUnicode4BytesUTF8Fail(self):
        input = b"\xfd\xbf\xbf\xbf\xbf\xbf"
        try:
            enc = ultrajson.encode(input)
            assert False, "Expected exception"
        except OverflowError:
            pass

    def test_encodeNullCharacter(self):
        input = "31337 \x00 1337"
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

        input = "\x00"
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

        self.assertEqual('"  \\u0000\\r\\n "', ultrajson.dumps("  \u0000\r\n "))

    def test_decodeNullCharacter(self):
        input = "\"31337 \\u0000 31337\""
        self.assertEqual(ultrajson.decode(input), json.loads(input))

    def test_encodeListLongConversion(self):
        input = [9223372036854775807, 9223372036854775807, 9223372036854775807,
                 9223372036854775807, 9223372036854775807, 9223372036854775807 ]
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeListLongUnsignedConversion(self):
        input = [18446744073709551615, 18446744073709551615, 18446744073709551615]
        output = ultrajson.encode(input)

        self.assertEqual(input, json.loads(output))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeLongConversion(self):
        input = 9223372036854775807
        output = ultrajson.encode(input)
        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_encodeLongUnsignedConversion(self):
        input = 18446744073709551615
        output = ultrajson.encode(input)

        self.assertEqual(input, json.loads(output))
        self.assertEqual(output, json.dumps(input))
        self.assertEqual(input, ultrajson.decode(output))

    def test_numericIntExp(self):
        input = "1337E40"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_numericIntFrcExp(self):
        input = "1.337E40"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_decodeNumericIntExpEPLUS(self):
        input = "1337E+9"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_decodeNumericIntExpePLUS(self):
        input = "1.337e+40"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_decodeNumericIntExpE(self):
        input = "1337E40"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_decodeNumericIntExpe(self):
        input = "1337e40"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_decodeNumericIntExpEMinus(self):
        input = "1.337E-4"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_decodeNumericIntExpeMinus(self):
        input = "1.337e-4"
        output = ultrajson.decode(input)
        self.assertEqual(output, json.loads(input))

    def test_dumpToFile(self):
        f = StringIO()
        ultrajson.dump([1, 2, 3], f)
        self.assertEqual("[1,2,3]", f.getvalue())

    def test_dumpToFileLikeObject(self):
        class filelike:
            def __init__(self):
                self.bytes = ''
            def write(self, bytes):
                self.bytes += bytes
        f = filelike()
        ultrajson.dump([1, 2, 3], f)
        self.assertEqual("[1,2,3]", f.bytes)

    def test_dumpFileArgsError(self):
        try:
            ultrajson.dump([], '')
        except TypeError:
            pass
        else:
            assert False, 'expected TypeError'

    def test_loadFile(self):
        f = StringIO("[1,2,3,4]")
        self.assertEqual([1, 2, 3, 4], ultrajson.load(f))

    def test_loadFileLikeObject(self):
        class filelike:
            def read(self):
                try:
                    self.end
                except AttributeError:
                    self.end = True
                    return "[1,2,3,4]"
        f = filelike()
        self.assertEqual([1, 2, 3, 4], ultrajson.load(f))

    def test_loadFileArgsError(self):
        try:
            ultrajson.load("[]")
        except TypeError:
            pass
        else:
            assert False, "expected TypeError"

    def test_version(self):
        assert re.match(r'^\d+\.\d+(\.\d+)?$', ultrajson.__version__), \
               "ultrajson.__version__ must be a string like '1.4.0'"

    def test_encodeNumericOverflow(self):
        try:
            ultrajson.encode(12839128391289382193812939)
        except OverflowError:
            pass
        else:
            assert False, "expected OverflowError"

    def test_encodeNumericOverflowNested(self):
        for n in range(0, 100):
            class Nested:
                x = 12839128391289382193812939

            nested = Nested()

            try:
                ultrajson.encode(nested)
            except OverflowError:
                pass
            else:
                assert False, "expected OverflowError"

    def test_decodeNumberWith32bitSignBit(self):
        #Test that numbers that fit within 32 bits but would have the
        # sign bit set (2**31 <= x < 2**32) are decoded properly.
        boundary1 = 2**31
        boundary2 = 2**32
        docs = (
            '{"id": 3590016419}',
            '{"id": %s}' % 2**31,
            '{"id": %s}' % 2**32,
            '{"id": %s}' % ((2**32)-1),
        )
        results = (3590016419, 2**31, 2**32, 2**32-1)
        for doc,result in zip(docs, results):
            self.assertEqual(ultrajson.decode(doc)['id'], result)

    def test_encodeBigEscape(self):
        for x in range(10):
            if PY3:
                base = '\\u00e5'.encode('utf-8')
            else:
                base = "\xc3\xa5"
            input = base * 1024 * 1024 * 2
            output = ultrajson.encode(input)

    def test_decodeBigEscape(self):
        for x in range(10):
            if PY3:
                base = '\\u00e5'.encode('utf-8')
                quote = "\"".encode()
            else:
                base = "\xc3\xa5"
                quote = "\""
            input = quote + (base * 1024 * 1024 * 2) + quote
            output = ultrajson.decode(input)

    def test_toDict(self):
        d = {"key": 31337}

        class DictTest:
            def toDict(self):
                return d

        o = DictTest()
        output = ultrajson.encode(o)
        dec = ultrajson.decode(output)
        self.assertEqual(dec, d)

    def test_decodeArrayTrailingCommaFail(self):
        input = "[31337,]"
        try:
            ultrajson.decode(input)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeArrayLeadingCommaFail(self):
        input = "[,31337]"
        try:
            ultrajson.decode(input)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeArrayOnlyCommaFail(self):
        input = "[,]"
        try:
            ultrajson.decode(input)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeArrayUnmatchedBracketFail(self):
        input = "[]]"
        try:
            ultrajson.decode(input)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeArrayEmpty(self):
        input = "[]"
        obj = ultrajson.decode(input)
        self.assertEqual([], obj)

    def test_decodeArrayDict(self):
        input = "{}"
        obj = ultrajson.decode(input)
        self.assertEqual({}, obj)

    def test_decodeArrayOneItem(self):
        input = "[31337]"
        ultrajson.decode(input)

    def test_decodeLongUnsignedValue(self):
        input = "18446744073709551615"
        ultrajson.decode(input)

    def test_decodeBigValue(self):
        input = "9223372036854775807"
        ultrajson.decode(input)

    def test_decodeSmallValue(self):
        input = "-9223372036854775808"
        ultrajson.decode(input)

    def test_decodeTooBigValue(self):
        try:
            input = "18446744073709551616"
            ultrajson.decode(input)
        except ValueError as e:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeTooSmallValue(self):
        try:
            input = "-90223372036854775809"
            ultrajson.decode(input)
        except ValueError as e:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeVeryTooBigValue(self):
        try:
            input = "18446744073709551616"
            ultrajson.decode(input)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeVeryTooSmallValue(self):
        try:
            input = "-90223372036854775809"
            ultrajson.decode(input)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeWithTrailingWhitespaces(self):
        input = "{}\n\t "
        ultrajson.decode(input)

    def test_decodeWithTrailingNonWhitespaces(self):
        try:
            input = "{}\n\t a"
            ultrajson.decode(input)
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeArrayWithBigInt(self):
        try:
            ultrajson.loads('[18446744073709551616]')
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeArrayFaultyUnicode(self):
        try:
            ultrajson.loads('[18446744073709551616]')
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_decodeFloatingPointAdditionalTests(self):
        self.assertEqual(-1.1234567893, ultrajson.loads("-1.1234567893"))
        self.assertEqual(-1.234567893, ultrajson.loads("-1.234567893"))
        self.assertEqual(-1.34567893, ultrajson.loads("-1.34567893"))
        self.assertEqual(-1.4567893, ultrajson.loads("-1.4567893"))
        self.assertEqual(-1.567893, ultrajson.loads("-1.567893"))
        self.assertEqual(-1.67893, ultrajson.loads("-1.67893"))
        self.assertEqual(-1.7893, ultrajson.loads("-1.7893"))
        self.assertEqual(-1.893, ultrajson.loads("-1.893"))
        self.assertEqual(-1.3, ultrajson.loads("-1.3"))

        self.assertEqual(1.1234567893, ultrajson.loads("1.1234567893"))
        self.assertEqual(1.234567893, ultrajson.loads("1.234567893"))
        self.assertEqual(1.34567893, ultrajson.loads("1.34567893"))
        self.assertEqual(1.4567893, ultrajson.loads("1.4567893"))
        self.assertEqual(1.567893, ultrajson.loads("1.567893"))
        self.assertEqual(1.67893, ultrajson.loads("1.67893"))
        self.assertEqual(1.7893, ultrajson.loads("1.7893"))
        self.assertEqual(1.893, ultrajson.loads("1.893"))
        self.assertEqual(1.3, ultrajson.loads("1.3"))

    def test_encodeBigSet(self):
        s = set()
        for x in range(0, 100000):
            s.add(x)
        ultrajson.encode(s)

    def test_encodeBlist(self):
        try:
            from blist import blist
        except ImportError:
            return

        b = blist(list(range(10)))
        c = ultrajson.dumps(b)
        d = ultrajson.loads(c)

        self.assertEqual(10, len(d))

        for x in range(10):
            self.assertEqual(x, d[x])

    def test_encodeEmptySet(self):
        s = set()
        self.assertEqual("[]", ultrajson.encode(s))

    def test_encodeSet(self):
        s = set([1,2,3,4,5,6,7,8,9])
        enc = ultrajson.encode(s)
        dec = ultrajson.decode(enc)

        for v in dec:
            self.assertTrue(v in s)

    def test_ReadBadObjectSyntax(self):
        try:
            ultrajson.loads('{"age", 44}')
        except ValueError:
            pass
        else:
            assert False, "expected ValueError"

    def test_ReadTrue(self):
        self.assertEqual(True, ultrajson.loads("true"))

    def test_ReadFalse(self):
        self.assertEqual(False, ultrajson.loads("false"))

    def test_ReadNull(self):
        self.assertEqual(None, ultrajson.loads("null"))

    def test_WriteTrue(self):
        self.assertEqual("true", ultrajson.dumps(True))

    def test_WriteFalse(self):
        self.assertEqual("false", ultrajson.dumps(False))

    def test_WriteNull(self):
        self.assertEqual("null", ultrajson.dumps(None))

    def test_ReadArrayOfSymbols(self):
        self.assertEqual([True, False, None], ultrajson.loads(" [ true, false,null] "))

    def test_WriteArrayOfSymbolsFromList(self):
        self.assertEqual("[true,false,null]", ultrajson.dumps([True, False, None]))

    def test_WriteArrayOfSymbolsFromTuple(self):
        self.assertEqual("[true,false,null]", ultrajson.dumps((True, False, None)))

    @unittest.skipIf(not PY3, "Only raises on Python 3")
    def test_encodingInvalidUnicodeCharacter(self):
        s = "\\udc7f"
        self.assertRaises(UnicodeEncodeError, ultrajson.dumps, s)

    def test_sortKeys(self):
        data = {"a": 1, "c": 1, "b": 1, "e": 1, "f": 1, "d": 1}
        sortedKeys = ultrajson.dumps(data, sort_keys=True)
        self.assertEqual(sortedKeys, '{"a":1,"b":1,"c":1,"d":1,"e":1,"f":1}')

"""
def test_decodeNumericIntFrcOverflow(self):
input = "X.Y"
raise NotImplementedError("Implement this test!")


def test_decodeStringUnicodeEscape(self):
input = "\\u3131"
raise NotImplementedError("Implement this test!")

def test_decodeStringUnicodeBrokenEscape(self):
input = "\\u3131"
raise NotImplementedError("Implement this test!")

def test_decodeStringUnicodeInvalidEscape(self):
input = "\\u3131"
raise NotImplementedError("Implement this test!")

def test_decodeStringUTF8(self):
input = "someutfcharacters"
raise NotImplementedError("Implement this test!")

"""

if __name__ == "__main__":
    unittest.main()


"""
# Use this to look for memory leaks
if __name__ == '__main__':
    from guppy import hpy
    hp = hpy()
    hp.setrelheap()
    while True:
        try:
            unittest.main()
        except SystemExit:
            pass
        heap = hp.heapu()
        print heap

"""
