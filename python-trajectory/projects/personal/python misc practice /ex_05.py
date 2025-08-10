num = 5
tot = 0.0
while True :
    sval =  input('enter a number:   ')
    if sval == 'done' :
        break
    try:
        fval = float(sval)
    except:
        print('invlid input')
        continue

    fval = float(sval)
    print(fval)
    num = num + 1
    tot = tot + fval

print(tot,num,tot/num)