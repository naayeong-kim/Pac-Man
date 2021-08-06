# enter your names and student numbers below
# Nayeong Kim       (s1006313)
# Chantal van Duin  (s1004516)


import exceptions

fruit_prices = {'apples': 2.00,
                'oranges': 1.50,
                'pears': 1.75,
                'limes': 0.75,
                'strawberries': 1.00}


def order_price(order):
    """
    Calculate the total price of the order. That is, the sum of the price of each fruit in the order times the amount.
    :param order: a list of (fruit, amount) tuples
    """
    cost = 0
    for fruit, amount in order:
        if fruit in fruit_prices:
            cost += fruit_prices[fruit] * amount
        else:
            return None
    return cost

def quicksort(lst):
    if len(lst) <= 1:
        return lst
    pivot = lst[0]
    smaller, bigger, equal = [], [], []
    for item in lst:
        if item > pivot:
            bigger.append(item)
        elif item < pivot:
            smaller.append(item)
        else:
            equal.append(item)
    print(f'{smaller} + {equal} + {bigger}')
    return quicksort(smaller) + equal + quicksort(bigger)
    raise exceptions.EmptyBonusAssignmentError


if __name__ == '__main__':
    order1 = [('apples', 2), ('pears', 3), ('limes', 4)]
    print(f'Cost of {order1} is {order_price(order1)}')

    order2 = [('pears', 2), ('limes', 1), ('strawberries', 10), ('melons', 3)]
    print(f'Cost of {order2} is {order_price(order2)}')

    order3 = [62, 4, 2, 1, 281 ,7, 21, 10, 10, 0, 18]
    print(f'Order: {order3}')
    print(f'Quick Sort: {quicksort(order3)}')