# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 10:00:39 2020
@author: polik
Scheme with 2 groups of reserved processors, 3 speeds
"""

from prettytable import PrettyTable
import math


def get_R1(m, k, l, z, u):
    """ Get upper bound for R1 """
    r = math.floor((m - k - l - 1) / (k * (z - 1) + l * (u - 1)))
    if r * (k * (z - 1) + l * (u - 1)) == m - k - l:
        r -= 1
    if r < 0:
        return -1
    else:
        return r


def get_R2(r1, m, k, l, z, u):
    """ Get upper bound for R2 """
    r = math.floor((m - k - l - 1) / (k * (z - 1) + l * (u - 1))) - r1
    if r * (k * (z - 1) + l * (u - 1)) == m - k - l - r1 * (k * (z - 1) + l * (u - 1)):
        r -= 1
    if r < 0:
        return -1
    else:
        return r


def get_PHI(B, R1, R2, m, k, l, s, t):
    """ Get upper bound for phi """
    z = math.ceil(s)
    u = math.ceil(t)
    phi = 1 - (t * l + s * k + m - k - l - t * l * (B - 1) - s * k * (B - t / s)) / (B * (m - k - l - (R1 + R2) * (k * (z - 1) + l * (u - 1))))
    if phi <= 0:
        return -1
    else:
        return min(phi, 1)


def check_condition(phi, psi, B, R1, R2, n, t):
    """ Check whether the specified condition holds """
    if (1 - phi) * B <= (psi * B) ** R1 * (B - t) and (1 - phi) * B <= (phi * B) ** (n * R2) * (B - n * psi * B):
        return True
    else:
        #print((1 - phi) * B, (psi * B) ** R1 * (B - t), (phi * B) ** (n * R2) * (B - n * psi * B))
        return False


def get_param(B, m, k, l, s, t):
    """ Search for parameters R1, R2, n, phi, psi """
    z = math.ceil(s)
    u = math.ceil(t)
    r1_max = get_R1(m, k, l, z, u)
    if r1_max == -1:
        return False

    for r1 in range(0, r1_max + 1):
        r2_max = get_R2(r1, m, k, l, z, u)

        if r2_max == -1:
            continue
        for r2 in range(0, r2_max + 1):
            phi_max = get_PHI(B, r1, r2, m, k, l, s, t)
            print(r1,r2, phi_max)
            if r1 ==2 and r2 ==0:
                print('ho')
            if phi_max == -1:
                continue
            phi = 0.001
            delta = 0.001
            while phi <= phi_max:
                if abs(phi - 0.657) <= 0.0001 and r1 == 2:
                    print("ho")
                psi = phi
                while psi <= 1:
                    n = 1
                    while n <= 1 / psi:
                        if check_condition(phi, psi, B, r1, r2, n, t):
                            #print(phi, psi, r1, r2, l)
                            return True
                        n += 1
                    psi += delta
                phi += delta
    return False

def get_B(m, k, l, s, t):
    """ Binary search on parameter B """
    eps = 0.0001
    c1 = 3
    c2 = 5
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
            print("good", c1, c2)
            if c2 - c1 < eps:
                if get_param(c, m, k, l, s, t):
                    return c
                else:
                    return c2
        else:
            c1 = c
            c = (c1 + c2) / 2
            print("bad", c1, c2)
            if c2 - c1 < eps:
                if get_param(c, m, k, l, s, t):
                    return c
                else:
                    return c2


speed1 = 2
speed2 = 3
L = 1
#print(get_R1(45, 5, 1, 2, 3))
#print(get_PHI(3.24609375, 2, 0, 45, 5, 1, 2, 3))
#print(check_condition(0.657000000005, 0.657000000005, 3.24609375, 2, 0, 1, 3))
#print(get_param(3.24609375, 45,5,1,2,3))
#print(get_B(45,5,1,2,3))
#print(get_B(28, 2, L, speed1, speed2))
tab = PrettyTable()
col = [str("Unit: " + str(i)) for i in range(30, 50)]
tab.add_column(" ", col)
n = 0
for k in range(1, 6):
    col = []
    for m in range(k + 30, k + 50):
        B = get_B(m, k, L, speed1, speed2)

        if B is not None:
            col.append(round(B, 4))
        else:
            col.append(-1)
        n += 1
        print(f"Done calculations: {n} / 50")
    tab.add_column(str("Accelerated: " + str(k)), col)


f = open("2_res_group-3(table).txt", "w+")
f.write(str(tab))
f.close()

