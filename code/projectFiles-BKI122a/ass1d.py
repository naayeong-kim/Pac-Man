# enter your names and student numbers below
# Nayeong Kim       (s1006313)
# Chantal van Duin  (s1004516)

import albertHeijn  # contains AlbertHeijn class


def permutations(elements, current=None, orders=None):
    """
    Given a list of elements, recursively calculate all possible orders of those elements.
    For example given three elements A, B and C, the result is:
    [[A, B, C], [A, C, B], [B, A, C], [B, C, A], [C, A, B], [C, B, A]]
    :param elements: the list of elements
    :param current: the list that is currently being recursively constructed
    :return: all permutations
    """
    if current is None:
        current = []
    if orders is None:
        orders = []
    subOrder = []
    if len(elements) == 0:  # if there are no more elements to add:
        subOrder += current.copy()  # add a copy of the current order to the list of orders
        orders.append(current.copy())
    for i in range(len(elements)):  # for each index in remaining elements, do:
        current.append(elements.pop(i))  # prepare: move the element at the index from the remaining list to the current order
        subOrder += permutations(elements, current, orders)  # recursively generate all following orders
        # repair: move the element from the current order back to the index on the remaining list
        elements.insert(i, current.pop())
    return orders  # return all generated orders


def path_distance(ahpath):
    """
    Given a path (list) of Albert Heijns, return the total distance of the path.
    """
    total_dist = 0
    for i in range(1, len(ahpath)):  # 'i' starts at 1, ends at last index of 'ahpath'
        total_dist += albertHeijn.distance(ahpath[i - 1].position(), ahpath[i].position())
    return total_dist


# some Albert Heijns in Nijmegen
albertheijns = [
    albertHeijn.AlbertHeijn('Daalseweg', 85, 77),
    albertHeijn.AlbertHeijn('Groenestraat', 68, 69),
    albertHeijn.AlbertHeijn('van Schevichavenstraat', 79, 83),
    albertHeijn.AlbertHeijn('St. Jacobslaan', 70, 58),
    albertHeijn.AlbertHeijn('Stationsplein', 70, 82)
]


def main():
    # print the path along all Albert Heijns with the minimum total distance
    key = path_distance(albertheijns)
    print(f'key : {key}')
    # start by generating all possible paths along all Albert Heijns
    paths = permutations(albertheijns)
    # take the minimum of the paths, using the path distance function to compare paths
    min_distance_path = min(paths, key=path_distance)
    # print the index (starting at 1) followed by the name of each Albert Heijn in the path
    for i, ah in enumerate(min_distance_path):
        print(i + 1, ah.name)


if __name__ == '__main__':
    paths = permutations(albertheijns)
    print(f'path : {paths}')
    main()