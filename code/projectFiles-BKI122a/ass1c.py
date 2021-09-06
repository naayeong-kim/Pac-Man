# enter your names and student numbers below
# Nayeong Kim       (s1006313)
# Chantal van Duin  (s1004516)


import exceptions
import shop  # contains FruitShop class


def shop_smart(order, shops):
    """
    Calculate at which shop the given order is cheapest.
    :param order: a list of (fruit, amount) tuples
    :param shops: a list of FruitShops
    :return: the shop that at which the order is cheapest
    """
    cost1 = 0
    cost2 = 0
    for fruit, price in order:
        cost1 += shops[0].cost_per_unit(fruit) * price
        cost2 += shops[1].cost_per_unit(fruit) * price
    if cost1 > cost2:
        return shops[1]
    else:
        return shops[0]
    raise exceptions.EmptyAssignmentError


def main():
    fruits1 = {'apples': 2.0, 'oranges': 1.0}
    fruits2 = {'apples': 1.0, 'oranges': 5.0}
    shop1 = shop.FruitShop('shop1', fruits1)
    shop2 = shop.FruitShop('shop2', fruits2)
    shops = [shop1, shop2]
    order1 = [('apples', 1.0), ('oranges', 3.0)]
    order2 = [('apples', 3.0)]
    print(f'For order {order1} the best shop is {shop_smart(order1, shops).name}.')
    print(f'For order {order2} the best shop is {shop_smart(order2, shops).name}.')


if __name__ == '__main__':
    main()
