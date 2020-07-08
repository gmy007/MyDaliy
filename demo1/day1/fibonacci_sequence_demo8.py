def fibonacci(num):
    count = 0
    a, b = 0, 1
    while count < num:
        yield b
        count += 1
        a, b = b, a + b

for i in fibonacci(5):
    print i
