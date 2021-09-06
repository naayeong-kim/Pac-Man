import shop

"""
A script that instantiates some shops other than those in shop.py
"""
    
shopName = 'the Berkeley Bowl'
fruitPrices = {'apples': 1.00, 'oranges': 1.50, 'pears': 1.75}
berkeleyShop = shop.FruitShop(shopName, fruitPrices)
applePrice = berkeleyShop.cost_per_unit('apples')
print(applePrice)
print(f'Apples cost €{applePrice:0.2f} at {shopName}.')

otherName = 'the Stanford Mall'
otherFruitPrices = {'kiwis':6.00, 'apples': 4.50, 'peaches': 8.75}
otherFruitShop = shop.FruitShop(otherName, otherFruitPrices)
otherPrice = otherFruitShop.cost_per_unit('apples')
print(otherPrice)
print(f'Apples cost €{otherPrice:0.2f} at {otherName}.')
print("My, that's expensive!")
