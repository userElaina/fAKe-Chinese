from fakecn import *
for i in range(20):
    print(fake())
    a=Faker()
    print(a.json())
    if a.verify():
        print(a.verify())
        raise Exception('What the f**k')