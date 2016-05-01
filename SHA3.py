#!/usr/bin/env python
import numpy as np
# Auxillary routine #1
# Expands one-dimensional array into three-dimensional array
def oneToThree(v):
    a = np.zeros((5, 5, 64)) # Initialize empty 5x5x64 array
    for i in range(5):
        for j in range(5):
            for k in range(64):
                a[i][j][k] = v[64*(5*j + i) + k]
    return a
# Auxillary routine #2
# Collapses three-dimensional array into one-dimensional array
def threeToOne(a):
    v = np.zeros(1600) # Initialize empty array of size 1600
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
    aout = np.zeros((5, 5, 64)) # Initialize empty 5x5x64 array
    for i in range(5):
        for j in range(5):
            for k in range(64):
                # XOR with result of sub-routine
                aout[i][j][k] = np.bitwise_xor(ain[i][j][k], thetaHelper(ain, i, j, k))
    return aout
# Rho
def rho(ain):
    rhomatrix=[[0,36,3,41,18],[1,44,10,45,2],[62,6,43,15,61],[28,55,25,21,56],[27,20,39,8,14]]
    rhom = np.array(rhomatrix) # Convert array into numpy's array class (for convenience)
    aout = np.zeros((5,5,64)) # Initialize empty 5x5x64 array

    for i in range(5):
        for j in range(5):
            for k in range(64):
                select = rhom[i][j] # Use lookup table to "calculate" (t + 1)(t + 2)/2
                aout[i][j][k] = ain[i][j][k - select]

    return aout
# Pi
def pi(ain):
    aout = np.zeros((5,5,64)) # Initialize empty 5x5x64 array
    
    for i in range(5):
        for j in range(5):
            for k in range(64):
                aout[j][(2*i+3*j)%5][k] = ain[i][j][k]
    return aout
