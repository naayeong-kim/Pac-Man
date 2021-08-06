# enter your names and student numbers below
# Nayeong Kim       (s1006313)
# Chantal van Duin  (s1004516)

import exceptions
import shop

def shop_loop():
    """
    Print the same output as running `python shop.py` using a for loop.
    """
    shop_names = ['Aldi', 'Albert Heijn']
    shop_prices = [{'apples': 1.00, 'oranges': 1.50, 'pears': 1.75},
                   {'kiwis': 6.00, 'apples': 4.50, 'peaches': 8.75}]
    for x in range(len(shop_names)):
        name = shop_names[x]
        price = shop_prices[x]
        shopInfo = shop.FruitShop(name, price)
        apples = shopInfo.cost_per_unit('apples')
        print(f'Apples cost €{apples:.2f} at {shopInfo.name}.')
    return None
    raise exceptions.EmptyAssignmentError


if __name__ == '__main__':
    shop_loop()
