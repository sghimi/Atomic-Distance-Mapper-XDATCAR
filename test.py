import math
import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt


file = open('XDATCAR', 'r')
lines = file.readlines()
xdatcar = open('XDATCAR', 'r')
system = xdatcar.readline()
scale = float(xdatcar.readline().rstrip('\n'))

# import l - Bounds
arr_1 = np.array(
    [float(s)*scale for s in xdatcar.readline().rstrip('\n').split()])
arr_2 = np.array(
    [float(s)*scale for s in xdatcar.readline().rstrip('\n').split()])
arr_3 = np.array(
    [float(s)*scale for s in xdatcar.readline().rstrip('\n').split()])

v = arr_1[0]
bound = [arr_1[0], arr_2[1], arr_3[2]]
print("Bounds: ", bound)

element_names = xdatcar.readline().rstrip('\n').split()
element_numbers = xdatcar.readline().rstrip('\n').split()
list_of_elements = [[] for i in range(5)]
times = []


def convert(line):
    list = line.split()
    return list


def fill_lists(times, lines):
    count = 0
    lis = []
    for i in times:
        lis.append(int(i))

    lis.sort()

    all_lines = []
    for line in lines:
        if count > 7:
            x = line.split()
            l = []
            for i in x:
                i = float(i)
                l.append(i)
            all_lines.append(l)
        count += 1

    for t in range(len(element_names)):

        if t == 0:
            y = int(element_numbers[t])
            x = 0
            list_of_elements[t] = all_lines[x:y]

        else:
            y = y + int(element_numbers[t])
            x = x + int(element_numbers[t-1])
            list_of_elements[t] = all_lines[x:y]
    return None


count = 0
for line in lines:
    # getting towards the 6th line
    count += 1
    if count == 7:
        times = convert(line)
        fill_lists(times, lines)

# Create dictionary from list
element = dict(zip(element_names, list_of_elements))


def get_key(val):
    for key, value in element.items():
        if val == value:
            return key
    return "key doesn't exist"


# finds distances between two types of atoms
def find_distance(list1, list2, min, max):

    d_array = []
    key1 = get_key(list1)
    key2 = get_key(list2)
    # calculating distance w/ periodic boundry
    i = 1
    for x in list1:
        j = 1
        for y in list2:
            a = x[0]-y[0]
            if(abs(a) > bound[0]*0.5):
                a = bound[0] - a

            b = x[1]-y[1]
            if(abs(b) > bound[1]*0.5):
                b = bound[1] - b

            c = x[2]-y[2]
            if(abs(c) > bound[2]*0.5):
                c = bound[2] - c

            d = math.sqrt(a**2+b**2+c**2)*(v)
            #print(key1, i, key2, j, " : ", d)
            if(d <= max and d >= min):
                #text = (key1, i, key2, j, ":", d)
                text = (d)
                d_array.append(text)
            j += 1
        i += 1
    return d_array


def find_all_distances(min, max):
    my_str = " "
    pArray = []
    text = []
    itemList = []
    # iterate pairwise every 2 items
    res = list(combinations(element, 2))
    flat_list = [item for sublist in res for item in sublist]
    for item1, item2 in zip(flat_list[::2], flat_list[1::2]):
        text.append(find_distance(element[item1], element[item2], min, max))
        itemList.append(item1+item2)
    atomic_bond = dict(zip(itemList, text))
    return atomic_bond


# Generate histograms, prints values in the console.
atomic_bonds = find_all_distances(0, 10) #from 0 to 10
for key in atomic_bonds:
    plt.hist(atomic_bonds[key])
    plt.title(key)
    plt.show()
    print(key, " ", atomic_bonds[key])
