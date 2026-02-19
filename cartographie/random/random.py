#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
génératuer de nombre aléatoire
"""

import matplotlib.pyplot as plt

import random as r

"""
def random(seed, length):
    seed = seed

    array2 = []
    m = 123476723
    a = 5
    p = 3
    for i in range(length):
        array1 = []
        for j in range(length):

            rand = (seed * p + a) % m
            array1.append(rand)
            seed = rand
        array2.append(array1)
    return array2



x = random(12, 10000)
    

plt.imshow(x)
plt.show()

plt.hist(x[0])
plt.show()
"""

def random(seed, length):
    seed = seed

    array2 = []
    m = 123456789
    a = 1234563
    p = 456789
    for i in range(length):
        array1 = []
        for j in range(length):

            rand = ((seed * p + a) % m)
            array1.append(rand)
            seed = rand
        array2.append(array1)
    return array2

x = random(1000012345, 100)
    

plt.imshow(x)
plt.show()

x = [[r.uniform(0, 1) for i in range (100)]for i in range (100)]

plt.imshow(x)
plt.show()

