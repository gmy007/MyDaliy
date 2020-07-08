import re
class data:
    _data = {'a': 1, 'b': 2, 'c': 3}

    def __getitem__(self, key):
         return self._data[key]

    def __setitem__(self, key, value):
        self._data.__setitem__(key, value)

obj1=data()
print obj1['a']

s = '\u5468\u661f\u9170"'
print s
print u''.join(s)
print s.decode('unicode_escape')

new=u''
i=0
while True:
    if s[i]!='"':
       i+=1
    else:

        print type(new+s[0:i])
        break

print float('NaN')
print float('inf')
print float('Infinity')

NUMBER_RE = re.compile(
    r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?',
    (re.VERBOSE | re.MULTILINE | re.DOTALL))
match_number = NUMBER_RE.match

m = match_number('123.456e10',0)
if m is not None:
    integer, frac, exp = m.groups()
    if frac or exp:
        res = float(integer + (frac or '') + (exp or ''))
        print
    else:
        res = int(integer)

print '-'*100

BACKSLASH = {
    '"': u'"', '\\': u'\\', '/': u'/',
    'b': u'\b', 'f': u'\f', 'n': u'\n', 'r': u'\r', 't': u'\t',
}

print {u'\u5468\u661f\u661f': 1}.keys().__str__().decode('unicode_escape')
