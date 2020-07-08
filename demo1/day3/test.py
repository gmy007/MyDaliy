# -*- coding: utf-8
testJson1='{"status":"0000","message":"success","data":{"title":{"id":"001","name":"白菜"},"content":[{"id":"001","value":"你好白菜"},{"id":"002","value":"你好萝卜"}]}}'

testJson2='{"animal":"cat","color":"orange"}'

testJson3='{"eggCartoon":["egg","egg","egg","egg","egg","egg","egg",null,"egg",null,"egg"]}'

testJson4='{"\u5468\u661f\u661f":1}'

s = '\u5468\u661f\u9170"'
import jsonparser,json

decoder=jsonparser.JSONDecoder()

# print decoder.decode(testJson2) # OK

# print decoder.decode(testJson3) #OK

# print decoder.decode(testJson4)

# print u''+testJson4

#decoder.decode(testJson2)
jsonp=jsonparser.JSONParser()

jsonp.loads(testJson1.decode('utf-8'))

#jsonp.dump_file('d://456.txt')

#jsonp.load_file('d://123.txt')

#print jsonp.dump_dict()

print jsonp.dumps()
rt=json.loads(testJson1.decode('utf-8'))
print rt
print json.dumps(rt)