import numpy as np
from matplotlib import pyplot as plt
from math import *

MEASURES_NUMBER = 999

#Calculates the Hamming weight of the parameter, i.e. the number of '1' in binary
def hamming_weight(x):    
    return bin(x).count("1")

#Returns p and q the two prime numbers that compose N = p*q
def find_prime_factors(N):
    i = 2
    prime_factors = []
    
    while i < sqrt(N):
        if N%i != 0:
            i += 1
        else:
            N = N//i
            prime_factors.append(i)
            
    #If N > 1, no second factor was found : N = q
    if N > 1:
        prime_factors.append(N)
        
    return prime_factors
