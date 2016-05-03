#!/usr/bin/env python
# Evan Paul
# CSCI181
# An Python implementation of SHA-3
import numpy as np
from sys import exit
# Auxillary routine #1
# Expands one-dimensional array into three-dimensional array
def oneToThree(v):
    a = np.zeros((5, 5, 64), dtype = int) # Initialize empty 5x5x64 array
    for i in range(5):
        for j in range(5):
            for k in range(64):
                a[i][j][k] = v[64*(5*j + i) + k]
    return a
# Auxillary routine #2
# Collapses three-dimensional array into one-dimensional array
def threeToOne(a):
    v = np.zeros(1600, dtype = int) # Initialize empty array of size 1600
    for i in range(5):
        for j in range(5):
            for k in range(64):
                v[64*(5*j+i)+k] = a[i][j][k]
    return v
# Subroutine for theta (separated for clarity)
def thetaHelper(ain, i, j, k):
    # First "summation"
    a = np.bitwise_xor(ain[(i-1)%5][0][k], ain[(i-1)%5][1][k])
    b = np.bitwise_xor(ain[(i-1)%5][2][k], ain[(i-1)%5][3][k])
    c = np.bitwise_xor(a, b)
    first = np.bitwise_xor(c, ain[(i-1)%5][4][k])
    # Second "summation"
    d = np.bitwise_xor(ain[(i+1)%5][0][(k-1)%64], ain[(i+1)%5][1][(k-1)%64])
    e = np.bitwise_xor(ain[(i+1)%5][2][(k-1)%64], ain[(i+1)%5][3][(k-1)%64])
    f = np.bitwise_xor(d, e)
    second = np.bitwise_xor(f, ain[(i+1)%5][4][(k-1)%64])
    # XOR of results
    return np.bitwise_xor(first, second)
# Theta
def theta(ain):
    aout = np.zeros((5, 5, 64), dtype = int) # Initialize empty 5x5x64 array
    for i in range(5):
        for j in range(5):
            for k in range(64):
                # XOR with result of sub-routine
                aout[i][j][k] = np.bitwise_xor(ain[i][j][k], thetaHelper(ain, i, j, k))
    return aout
# Rho
def rho(ain):
    rhomatrix=[[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
    rhom = np.array(rhomatrix, dtype=int) # Convert LUT into numpy's array class (for convenience)
    aout = np.zeros((5,5,64), dtype = int) # Initialize empty 5x5x64 array

    for i in range(5):
        for j in range(5):
            for k in range(64):
                select = rhom[i][j] # Use lookup table to "calculate" (t + 1)(t + 2)/2
                aout[i][j][k] = ain[i][j][k - select]
    return aout
# Pi
def pi(ain):
    aout = np.zeros((5,5,64), dtype = int) # Initialize empty 5x5x64 array

    for i in range(5):
        for j in range(5):
            for k in range(64):
                aout[j][(2*i+3*j)%5][k] = ain[i][j][k]
    return aout
# Chi
def chi(ain):
    aout = np.zeros((5,5,64), dtype = int) # Initialize empty 5x5x64 array

    for i in range(5):
        for j in range(5):
            for k in range(64):
                xor = np.bitwise_xor(ain[(i+1)%5][j][k], 1)
                mul = xor * (ain[(i+2)%5][j][k])
                aout[i][j][k] = np.bitwise_xor(ain[i][j][k], mul)
    return aout
# Iota
def iota(ain, rnd):
    # Initialize empty arrays
    aout = np.zeros((5,5,64), dtype = int)
    bit = np.zeros(dtype = int, shape = (5,5,64))
    rc = np.zeros(dtype = int, shape = 168)

    # Linear Feedback Shift Register
    w = np.array([1,0,0,0,0,0,0,0], dtype = int)
    rc[0] = w[0]
    for i in range(1, 7*24):
        a = np.bitwise_xor(w[0], w[4])
        b = np.bitwise_xor(w[5], w[6])
        tail = np.bitwise_xor(a, b)
        w = [w[1],w[2],w[3],w[4],w[5],w[6],w[7], tail]
        rc[i] = w[0]
    # Calculate bits
    for l in range(7):
        q = pow(2, l) - 1
        t = l + 7*rnd
        bit[0][0][q] = rc[l + 7*rnd]
    # Calculate aout
    for i in range(5):
        for j in range(5):
            for k in range(64):
                aout[i][j][k] = np.bitwise_xor(ain[i][j][k], bit[i][j][k])
    return aout


# SHA-3 algorithm
def sha3(pt, padding = True):
    l = len(pt)

    # Convert to numpy format and resize
    v = np.array(pt, dtype = int)
    v.resize(1600)

    if padding:
        if l > 1086:
            sys.exit("Input must be less than or equal to 1086 bits")
        v[l] = 1
        v[1087] = 1

    a = oneToThree(v)
    for rounds in range(24):
        a = iota(chi(pi(rho(theta(a)))), rounds)

    return threeToOne(a)
