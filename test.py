import math
import numpy as np
from copy import deepcopy
from itertools import combinations
from scipy.spatial import distance


file = open('XDATCAR', 'r')
lines = file.readlines()

xdatcar = open('XDATCAR', 'r')
system = xdatcar.readline()
scale = float(xdatcar.readline().rstrip('\n'))

#import l - vectors
arr_1 = np.array(
    [float(s)*scale for s in xdatcar.readline().rstrip('\n').split()])
arr_2 = np.array(
    [float(s)*scale for s in xdatcar.readline().rstrip('\n').split()])
arr_3 = np.array(
    [float(s)*scale for s in xdatcar.readline().rstrip('\n').split()])

v = arr_1[0]
print("Box vectors sizes are ",arr_1,arr_2,arr_3)

element_names = xdatcar.readline().rstrip('\n').split()
element_numbers = xdatcar.readline().rstrip('\n').split()
list_of_elements = [[] for i in range(5)]
times = []

def convert(line):
    list = line.split()
    return list

# Fills the lists
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

# Return key for any value in dict
def get_key(val):
    for key, value in element.items():
        if val == value:
            return key
    return "key doesn't exist"

# finds distances between two types of atoms
def find_distance(list1, list2,min,max):
    key1 = get_key(list1)
    key2 = get_key(list2)

    # calculating distance
    i = 1
    for x in list1:
        j = 1
        for y in list2:
            a = x[0]-y[0]
            a = a*a
            b = x[1]-y[1]
            b = b*b
            c = x[2]-y[2]
            c = c*c
            d = math.sqrt(a+b+c)*(v)
            #print(key1, i, key2, j, " : ", d)
            if(d <= max and d >= min ):
                print(key1, i, key2, j, " : ", d)
            j += 1
        i += 1

def find_all_distances(min,max):
    # iterate pairwise every 2 items
    res = list(combinations(element, 2))
    flat_list = [item for sublist in res for item in sublist]
    print(flat_list)
    for item1, item2 in zip(flat_list[::2], flat_list[1::2]):
        find_distance(element[item1], element[item2],min,max)


#finds bonds with distance from 1-3
find_all_distances(1,3)