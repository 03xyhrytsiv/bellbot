from example import *


print("Welcome to De Luxe Cafe Telegram bot")
print("Enter your order, please, using comma")
check = True
order = input()
order = " " + order
orderLst = []
while check:
    el = order.find(",")
    if el == -1:
        orderLst.append(order)
        check = False
    else:
        orderLst.append(order[0:el])
        order = order[(el+1):]

finalOrder = []
for i in orderLst:
    if " " in i:
        i = i[1:]
        finalOrder.append(i)
    else:
        finalOrder.append(i)

for i in finalOrder:
    while i not in wholeMenu:
        print(str(i) + " is not in our menu")
        new = input("Enter it in the right way or print '-': ")
        if new == '-':
            finalOrder.remove(i)
            break
        elif new in wholeMenu:
            finalOrder.remove(i)
            finalOrder.append(new)
            break
        i = new

print("Here is your order: ")
print("--------------------")
for i in finalOrder:
    print(i)
print("--------------------")
print("Thanks for ordering!")
