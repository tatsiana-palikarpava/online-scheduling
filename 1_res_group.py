# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:00:39 2020
@author: polik
Scheme with 1 group of reserved processors, 2 speeds
"""

from prettytable import PrettyTable
import math


def get_R(m, k, z, x):
    """ Get upper bound for R """
    r = math.floor((m - k - 1) / (k * (z - 1) + x))
    if r * (k * (z - 1) + x) == m - k:
        r -= 1
    if r < 1:
        return -1
    else:
        return r


def get_PHI(B, R, m, k, s, x):
    """ Get upper bound for phi """
    z = math.ceil(s)
    phi = 1 - (s * k + m - k - s * k * (B - 1)) / (B * (m - k - R * (k * (z - 1) + x)))
    if phi <= 0:
        return -1
    else:
        return min(phi, 1)


def get_PSI(B, phi, k, z, x, l):
    """ Get upper bound for psi"""
    w = math.floor((x * l) / ((z - 1) * k))
    if x == 0:
        return 1 / B
    else:
        psi = (phi * B) ** w / B
        if psi <= 0:
            return -1
        else:
            return min(psi, 1 / l, 1)


def check_condition(phi, psi, B, R, l, s):
    """ Check whether the specified condition holds """
    if (1 - phi) * B <= (psi * B) ** R * min((B - s), B * (1 - l * psi)):
        return True
    else:
        return False


def get_param(B, m, k, s):
    """ Search for parameters R, x, l, phi, psi """
    z = math.ceil(s)
    # Case R = 0
    phi_max = get_PHI(B, 0, m, k, s, 0)
    if phi_max != -1:
        phi = 0.001
        delta = 0.001
        while phi <= phi_max:
            psi = phi
            if check_condition(phi, psi, B, 0, 1, s):
                # print(x, 1, phi, psi, 0)
                return True
            phi += delta
    # Case R != 0
    if m - z * k > 1:
        # Search for x
        for x in range(1, m - z * k):
            r_max = get_R(m, k, z, x)
            if r_max == -1:
                continue
            else:
                for r in range(1, r_max + 1):
                    phi_max = get_PHI(B, r, m, k, s, x)
                    if phi_max == -1:
                        continue
                    phi = 0.001
                    delta = 0.001
                    while phi <= phi_max:
                        l = 1
                        while l <= 1 / phi:
                            psi_max = get_PSI(B, phi, k, z, x, l)
                            if psi_max == -1:
                                l += 1
                                continue
                            else:
                                psi = phi
                                while psi <= psi_max:
                                    if check_condition(phi, psi, B, r, l, s):
                                        # print(x, l, phi, psi, r)
                                        return True
                                    psi += delta
                            l += 1
                        phi += delta

    return False
    """else:
        phi_max = get_PHI(B, 0, m, k, z, 0)
        if phi_max != None:
            phi = 0.001
            delta = 0.001
            while phi <= phi_max:
                psi = phi
                if (check_condition(phi, psi, B, 0, 1)):
                    # print(x, l, phi, psi, 0)
                    return True
                phi += delta
        return False"""


def get_B(m, k, s):
    """ Binary search on parameter B """
    eps = 0.0001
    c1 = 1
    c2 = 10
    z = math.ceil(s)
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
            z = math.ceil(speed)
            B = get_B(m, k, speed)

            if B is not None:
                col.append(round(B, 4))
            else:
                col.append(-1)
            n += 1
            print(f"Done calculations: {n} / 50")
        tab.add_column(str("Fast: " + str(k)), col)
    f = open("1_res_group.txt", "w+")
    f.write(str(tab))
    f.close()
else:
    f = open("1_res_group-res(6-10).txt","w+")
    n = 0
    for m in range(30, 50):
        col = []
        for k in range(6, 11):
            B = get_B(m + k, k, speed)
            if B is not None:
                col.append(round(B, 4))
            else:
                col.append(-1)
            n += 1
            print(n)
        f.write(str(col)[1:-1] + '\n')
    f.close()
