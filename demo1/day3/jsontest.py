# -*- coding: utf-8
import json
testJson1='{"status":"0000","message":"success","data":{"title":{"id":"001","name":"白菜"},"content":[{"id":"001","value":"你好白菜"},{"id":"002","value":"你好萝卜"}]}}'

print type(testJson1.decode('utf-8'))
print json.loads(testJson1.decode('utf-8'))