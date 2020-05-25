# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:24:45 2020

@author: polik
"""

#read from files
from matplotlib import pyplot as plt
print("ho")
init = open('initial-2-res(very fast).txt', 'r')
mod = open('modified_group-res(very fast).txt', 'r')
k_range = 5
m_range = 200
M = [20 + i for i in range(m_range)]
Bs_init = [[0] * k_range for i in range(m_range)]
Bs_mod = [[0] * k_range for i in range(m_range)]
lines = init.readlines()
for i,line in enumerate(lines):
    line = line.strip()
    b = line.split(', ')
    b = [float(x) for x in b]
    for j in range(k_range):
        Bs_init[i][j] = b[j]

lines = mod.readlines()
for i,line in enumerate(lines):
    line = line.strip()
    b = line.split(', ')
    b = [float(x) for x in b]
    for j in range(k_range):
        Bs_mod[i][j] = b[j]

plt.figure()
plt.xlabel('Number of processors')
plt.ylabel('Estimated B')
for k in range(1, k_range + 1):
    plt.title('$s=4, k=$' + str(k))
    plt.plot(M, [row[k - 1] for row in Bs_init], 'r-', label='Initial scheme')
    plt.plot(M, [row[k - 1] for row in Bs_mod], 'c-', label='Modified group size')
    plt.legend()
    plt.show()
