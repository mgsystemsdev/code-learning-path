def step1(x): return x + 2
def step2(x): return x * 3
def step3(x): return x - 5

def pipeline(data):
    for step in [step1, step2, step3]:
        data = step(data)
    return data

print(pipeline(5))  # ((5+2)*3)-5 = 16



def make_adder(n):
    def adder(x):
        return x + n
    return adder

add5 = make_adder(5)
print(add5(10))  # 15
