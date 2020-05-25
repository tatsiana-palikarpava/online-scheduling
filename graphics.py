# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 12:24:45 2020

@author: polik
"""

#read from files
#from matplotlib import pyplot as plt
init = open('initial-2-res(6-10).txt', 'r')
res1 = open('1_res_group-res(6-10).txt', 'r')
res2 = open('2_res_group-res(6-10).txt', 'r')
mod = open('modified_group-res(6-10).txt', 'r')
k_range = 5
m_range = 20
M = [30 + i for i in range(m_range)]
Bs_init = [[0] * k_range for i in range(m_range)]
Bs_res1 = [[0] * k_range for i in range(m_range)]
Bs_res2 = [[0] * k_range for i in range(m_range)]
Bs_mod = [[0] * k_range for i in range(m_range)]
lines = init.readlines()
for i,line in enumerate(lines):
    line = line.strip()
    b = line.split(', ')
    b = [float(x) for x in b]
    for j in range(k_range):
        Bs_init[i][j] = b[j]

lines = res1.readlines()
for i,line in enumerate(lines):
    line = line.strip()
    b = line.split(', ')
    b = [float(x) for x in b]
    for j in range(k_range):
        Bs_res1[i][j] = b[j]

lines = res2.readlines()
for i,line in enumerate(lines):
    line = line.strip()
    b = line.split(', ')
    b = [float(x) for x in b]
    for j in range(k_range):
        Bs_res2[i][j] = b[j]

lines = mod.readlines()
for i,line in enumerate(lines):
    line = line.strip()
    b = line.split(', ')
    b = [float(x) for x in b]
    for j in range(k_range):
        Bs_mod[i][j] = b[j]
import matplotlib.pyplot as plt
plt.figure()
plt.xlabel('Number of processors')
plt.ylabel('Estimated B')
for k in range(1, k_range + 1):
    plt.title('$s=2, k=$' + str(k))
    plt.plot(M, [row[k - 1] for row in Bs_init], 'r-', label='Initial scheme')
    plt.plot(M, [row[k - 1] for row in Bs_res1], 'g-', label='1 reserved group')
    plt.plot(M, [row[k - 1] for row in Bs_res2], 'b-', label='2 reserved groups')
    plt.plot(M, [row[k - 1]+0.001 for row in Bs_mod], 'c-', label='Modified group size')
    plt.legend()
    plt.show()
