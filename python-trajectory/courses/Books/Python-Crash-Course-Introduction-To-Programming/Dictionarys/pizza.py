# a list of dictionaries

pizza = {
    'crust': 'thick',
    'toppings': ['mushrooms', 'extra cheese']
}


#sumarized your order


print(f"You ordered a {pizza['crust']}-crust pizza with the following toppings:")

for topping in pizza['toppings']:
    print(f"\t{topping}")

