# -*- coding: utf-8
import re,time
HAS_UTF8 = re.compile(r'[\x80-\xff]')
ESCAPE_ASCII = re.compile(r'([\\"]|[^\ -~])')
ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}

def encode_basestring_ascii(s):
    """Return an ASCII-only JSON representation of a Python string
    """
    if isinstance(s, str) and HAS_UTF8.search(s) is not None:
        s = s.decode('utf-8')

    def replace(match):
        s = match.group(0)
        try:
            return ESCAPE_DCT[s]
        # not in escape list
        except KeyError:
            n = ord(s)
            if n < 0x10000:  # TODO handle more than 32bit
                return '\\u{0:04x}'.format(n)
            else:
                raise AssertionError()

    # find Unicode and replace with ascii
    return '"' + str(ESCAPE_ASCII.sub(replace, s)) + '"'

#print encode_basestring_ascii()
print u'\u5468'

s1 = 0xd800
s2 = 0xdc00
print '\\u{0:4x}\\u{1:04x}'.format(s1, s2)

print '-'*100
print '\"'+u'''Sit qui mollit anim nisi ut Lorem esse cillum. Ullamco nisi aliquip non ullamco nulla culpa qui amet enim deserunt. Irure consectetur ad nisi do laborum sint deserunt amet enim esse enim fugiat in exercitation.
'''+'\"'
