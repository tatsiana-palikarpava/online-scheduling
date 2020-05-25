# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:00:39 2020
@author: polik
Scheme with modified group size, 2 speeds
"""

from prettytable import PrettyTable
import math


def get_R(m, k, y):
    """ Get upper bound for R """
    r = math.floor((m - k - 1) / (k * (y - 1)))
    if r * k * (y - 1) == m - k:
        r -= 1
    if r < 0:
        return -1
    else:
        return r


def get_PHI(B, R, m, k, y, s):
    """ Get upper bound for phi """
    phi = 1 - (s * k + m - k - s * k * (B - 1)) / (B * (m - k - R * k * (y - 1)))
    if phi <= 0:
        return -1
    else:
        return min(phi, 1)


def check_condition(phi, B, R, s, y):
    """ Check whether the specified condition holds """
    if (1 - phi) * B <= (min(phi * B, phi * B * (y / s))) ** R * (B - s):
        return True
    else:
        return False

def get_param(B, m, k, s):
    """ Search for parameters R, phi, y"""
    y = 2
    while y <= (m-k-1) / k + 1:
        r_max = get_R(m, k, y)
        if r_max == -1:
            continue
        for r in range(0, r_max + 1):
            phi_max = get_PHI(B, r, m, k, y, s)
            if phi_max == -1:
                continue
            phi = 0.001
            delta = 0.001
            while phi <= phi_max:
                if check_condition(phi, B, r, s, y):
                    return True
                phi += delta
        y += 1
    return False

def get_B(m, k, s):
    c1 = 1
    c2 = 5
    eps = 0.0001
    while (not get_param(c2, m, k, s)) and c2 < 100:
        c2 *= 2
    if c2 >= 100:
        return
    c = (c1 + c2) / 2
    while True:
        if get_param(c, m, k, s):
            c2 = c
            c = (c1 + c2) / 2
            if c2 - c1 < eps:
                if get_param(c, m, k, s):
                    return c
                else:
                    return c2
        else:
            c1 = c
            c = (c1 + c2) / 2
            if c2 - c1 < eps:
                if get_param(c, m, k, s):
                    return c
                else:
                    return c2


speed = 5
pretty = False
if pretty:
    tab = PrettyTable()
    col = [str("Unit: " + str(i)) for i in range(30, 50)]
    tab.add_column(" ", col)
    for k in range(1, 6):
        col = []
        for m in range (k+30, k+50):
                z = math.ceil(speed)
                B = get_B(m,k,z,speed)

                if B is not None:
                    col.append(round(B, 4))
                else:
                    col.append(-1)

        tab.add_column(str("Fast: " + str(k)),col)

        f= open("modified_group.txt","w+")
        f.write(str(tab))
        f.close()
else:
    f = open("modified_group-res(very fast).txt","w+")
    n = 0
    for m in range(20, 220):
        col = []
        for k in range(1, 6):
            B = get_B(m + k, k, speed)
            if B is not None:
                col.append(round(B, 4))
            else:
                col.append(speed + 1)
            n += 1
            print(n)
        f.write(str(col)[1:-1] + '\n')
    f.close()
