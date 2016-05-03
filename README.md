# pySHA
A Python implementation of the SHA-3 algorithm, written for CSCI181 (Applied Cryptography) with the assistance of Dr. Schaefer's excellent [lecture notes](http://math.scu.edu/~eschaefe/book.pdf) on the algorithm.

## Usage
This implementation may not match other, current implementations of SHA-3 due to updates of the algorithm or other reasons. The purpose of this repository is intended mostly for demonstration purposes rather than usage.

However, if you'd still like to use it, it's fairly straightforward:

+ Install numpy: `pip install numpy` *tip: use virtualenv*
+ Import the hash function into your code:
`from SHA3 import sha3`
+ Use it:
`sha3(plaintext)` where plaintext is a binary array (currently no other input format is accepted, so convert accordingly)

In this current iteration (which will most likely be updated), only the hash function, f, is provided. To fully implement the algorithm, follow the diagram in the subsequent section.
## The Algorithm
The input to the hash algorithm is padded until its length is a multiple of 1088. Each padded segment, P, is then appended with 512 zeroes and inputted into the hash function, f. Inputs with length > 1088 bits, are segmented and XOR'd as seen in the diagram:
![SHA3](http://i.imgur.com/jseyReF.png)

The hash function itself, f, consists of 24 rounds of the following composition of routines applied to each padded array of length 1600:

`ι ◦ χ ◦ π ◦ ρ ◦ θ`  

which is implemented simply by:
```python
for rounds in range(24):
        a = iota(chi(pi(rho(theta(a)))), rounds)
```
Explanations of each routine can be found in his notes, or just simply read through the code.
## Files
SHA3.py => Implementation of routines and algorithm  
test.py => Tests of each routine with sample data  
README.md  => You are here
