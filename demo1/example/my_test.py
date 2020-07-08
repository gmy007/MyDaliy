from jsonparser import JsonParser

parser = JsonParser()

file_path = 'tmp_output_file.txt'


def fun1():
    parser.loads('{"a": "\\u7f51\\u6613CC\\"\'"}')
    # parser.loads('{ "{ab" : "}123", "\\\\a[": "]\\\\"}')
    parser.dump_file(file_path)
    print  parser.dumps()
    parser2 = JsonParser()
    parser.load_file(file_path)
    print parser.dumps()

def fun2():
    s = '{ "{ab" : "}123", "\\\\a[": "]\\\\"}'
    # print s[20]
    for i ,j in enumerate(s):
        print i,j

if __name__ == '__main__':
    fun1()
    #fun2()