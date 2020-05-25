# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:00:39 2020
@author: polik
Scheme with 2 groups of reserved processors, 2 speeds
"""

from prettytable import PrettyTable
import math


def get_R1(m, k, z):
    """ Get upper bound for R1 """
    r = math.floor((m - k - 1) / (k * (z - 1)))
    if r * k * (z - 1) == m - k:
        r -= 1
    if r < 0:
        return -1
    else:
        return r


def get_R2(r1, m, k, z):
    """ Get upper bound for R2 """
    r = math.floor((m - k - 1) / (k * (z - 1))) - r1
    if r * k * (z - 1) == m - k - r1 * k * (z - 1):
        r -= 1
    if r < 0:
        return -1
    else:
        return r


def get_PHI(B, R1, R2, m, k, s):
    """ Get upper bound for phi """
    z = math.ceil(s)
    phi = 1 - (s * k + m - k - s * k * (B - 1)) / B / (m - k - (R1 + R2) * k * (z - 1))
    if phi <= 0:
        return -1
    else:
        return min(phi, 1)


def check_condition(phi, psi, B, R1, R2, l, s):
    """ Check whether the specified condition holds """
    if (1 - phi) * B <= (psi * B) ** R1 * (B - s) and (1 - phi) * B <= (phi * B) ** (l * R2) * (B - l * psi * B):
        return True
    else:
        return False


def get_param(B, m, k, s):
    """ Search for parameters R1, R2, l, phi, psi """
    z = math.ceil(s)
    r1_max = get_R1(m, k, z)
    if r1_max == -1:
        return False

    for r1 in range(0, r1_max + 1):
        r2_max = get_R2(r1, m, k, z)
        if r2_max == -1:
            continue
        for r2 in range(0, r2_max + 1):
            phi_max = get_PHI(B, r1, r2, m, k, s)
            if phi_max == -1:
                continue
            phi = 0.001
            delta = 0.01
            while phi <= phi_max:
                psi = phi
                while psi <= 1:
                    l = 1
                    while l < 1 / psi:
                        if (check_condition(phi, psi, B, r1, r2, l, s)):
                            #print(phi, psi, r1, r2, l)
                            return True
                        l += 1
                    psi += delta
                phi += delta
    return False

def get_B(m, k, s):
    """ Binary search on parameter B """
    eps = 0.01
    c1 = 1
    c2 = 5
    while (not get_param(c2,m,k,s)) and c2 < 100:
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
            if c2 - c1 < 0.01:
                if get_param(c, m, k, s):
                    return c
                else:
                    return c2



speed = 2
pretty = False
if pretty:
    tab = PrettyTable()
    col = [str("Unit: " + str(i)) for i in range(30, 40)]
    tab.add_column(" ", col)
    n = 0
    for k in range(1, 6):
        col = []
        for m in range(k + 30, k + 40):
            B = get_B(m, k, speed)

            if B is not None:
                col.append(round(B, 4))
            else:
                col.append(-1)
            n += 1
            print(f"Done calculations: {n} / 50")
        tab.add_column(str("Fast: " + str(k)), col)


    f = open("2_res_group.txt", "w+")
    f.write(str(tab))
    f.close()
else:
    f = open("2_res_group-res.txt","w+")
    for m in range(30, 50):
        col = []
        for k in range(1, 6):
            B = get_B(m + k, k, speed)
            if B is not None:
                col.append(round(B, 4))
            else:
                col.append(-1)
        f.write(str(col)[1:-1] + '\n')
    f.close()

