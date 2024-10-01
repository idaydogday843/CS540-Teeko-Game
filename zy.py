a = set([1, 2])
b = set([2, 3])
c = a.union(b)
print(a, b, c)

with open("a.txt", 'w') as f:
    f.write("!!")
with open("a.txt", 'r') as f:
    c = f.read()
    print(c)
    
def f():
    print("f")
def g():
    print("g")
def h():
    print("h")
h = g
g = f
f = h
f()

def f(n):
    def g(x):
        return x ** n
    return g

sum = 0
sum1 = 0
sum2 = 0
sum3 = 0
n = 100
for i in range(n):
    sum += f(i)(2)
    sum1 += 2 ** i
    sum2 += i ** 2
    sum3 += i * 2
print(sum)
print(sum1)
print(sum2)
print(sum3)