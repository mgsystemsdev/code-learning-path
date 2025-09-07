def shipping_cost(weight):
    if weight < 1:
        return {"price": "$5", "note": "Light package, fast delivery"}
    elif weight <= 5:
        return {"price": "$10", "note": "Standard package, normal delivery"}
    else:
        return {"price": "$20", "note": "Heavy package, expect slower delivery"}

order = shipping_cost(.9)
print(order["price"])
print(order["note"])
