# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:00:39 2020
@author: polik
Initial scheme, 3 speeds
"""

from prettytable import PrettyTable
import math

def get_R(m, k, l, z, u):
    """ Get upper bound for R """
    r = math.floor((m - k - l - 1) / (k * (z - 1) + l * (u - 1)))
    if r * (k * (z - 1) + l * (u - 1)) == m - k:
        r -= 1
    if r < 1:
        return -1
    else:
        return r

def get_PHI(B, R, m, k, l, s, t):
    """ Get upper bound for phi """
    z = math.ceil(s)
    u = math.ceil(t)
    phi = 1 - (s * k + t * l + m - k - l - t * l * (B - 1) - s * k * (B - t / s)) / (B * (m - k - l - R * (k * (z - 1) + l * (u - 1))))
    if phi <= 0:
        return -1
    else:
        return min(phi, 1)

def check_condition(phi, B, R, t):
    if (1 - phi) * B <= (phi * B) ** R * (B - t):
        return True
    else:
        return False

def get_param(B, m, k, l, s, t):
    """ Search for parameters R, phi"""
    z = math.ceil(s)
    u = math.ceil(t)
    R = get_R(m, k, l, z, u)
    if R != -1:
        for r in range(1, R + 1):
            phi1 = 0.001
            phi2 = get_PHI(B, r, m, k, l, s, t)
            delta = 0.001
            if phi2 != -1:
                while phi1 <= phi2:
                    if check_condition(phi1, B, r, t):
                        print(phi1, r)
                        return True
                    else:
                        phi1 += delta
    else:
        return False

def get_B(m, k, l, s, t):
    """ Binary search on parameter B """
    eps = 0.001
    c1 = 1
    c2 = 10
    z = math.ceil(s)
    while (not get_param(c2, m, k, l, s, t)) and c2 < 100:
        c2 *= 2
    if c2 >= 100:
        return
    c = (c1 + c2) / 2
    while True:
        if get_param(c, m, k, l, s, t):
            c2 = c
            c = (c1 + c2) / 2
            if c2 - c1 < eps:
                if get_param(c, m, k, l, s, t):
                    return c
                else:
                    return c2
        else:
            c1 = c
            c = (c1 + c2) / 2
            if c2 - c1 < eps:
                if get_param(c, m, k, l, s, t):
                    return c
                else:
                    return c2

speed1 = 2
speed2 = 3
l = 1

f = open("initial-3(table)(1).txt","w+")

tab = PrettyTable()
col = [str("Unit: " + str(i)) for i in range(30, 50)]
tab.add_column(" ", col)
for k in range(1, 6):
    col = []
    for m in range(k + 30, k + 50):
            B = get_B(m, k, l, speed1, speed2)
            if B is not None:
                col.append(round(B, 4))
            else:
                col.append(-1)

    tab.add_column(str("Accelerated: " + str(k)),col)

f.write(str(tab))
f.close()

#f = open("initial-3-res(high).txt","w+")
"""
n = 0
l = 1
for m in range(30, 50):
    col = []
    for k in range(1, 6):
        B = get_B(m + k, k, l, 2, 3)
        if B is not None:
           col.append(round(B, 4))
        else:
           col.append(4)
        n += 1
        print(n)
    f.write(str(col)[1:-1] + '\n')
f.close()
"""
