import json, re

data = [{'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}]

json2 = json.dumps(data)
print json
WHITESPACE = re.compile(r'\d+')
w=WHITESPACE.match


print w('123',0).end()

print  json.dumps({'a': 'Runoob', 'b': 7}, sort_keys=True, indent=4, separators=(',', ': '))

data2 = {'key': 'value', 'name': 'gmy', 'married': False, 'friends': ['sad', 'happy']}
str=json.dumps(data2)
print str

print
print float('nan')