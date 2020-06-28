# +, -, /, *, mod, pow, div, где

a = float(input('a = '))
b = float(input('b = '))
c = input('c = ')


if c == '/':
    if b == 0.0:
        print('Деление на 0!')
    else:
        print(a / b)

elif c == 'mod':
    if b == 0.0:
        print('Деление на 0!')
    else:
        print(a % b)

elif c == 'div':
    if b == 0.0:
        print('Деление на 0!')
    else:
        print(a // b)

elif c == '+':
    print(a + b)
elif c == '-':
    print(a - b)
elif c == '*':
    print(a * b)
elif c == 'pow':
    print(a ** b)
