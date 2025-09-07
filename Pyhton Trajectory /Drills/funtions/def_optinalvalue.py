

def greet(name="Miguel"):
    return f"Hello, {name}!"

print(greet())          
print(greet("Ericka"))  


def order_coffee(size="medium", type="latte"):
    # build your return message
    return f"Your {size} {type} is ready!"

order1 = order_coffee()
order2 = order_coffee("large")
order3 = order_coffee("small", "espresso")

print("")
print("")
print(order1)
print(order2)
print(order3)
print("")
print("")