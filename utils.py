import numpy as np
from matplotlib import pyplot as plt
from math import *

SET_NUMBER = "10"
KEY_SIZE = 32
MEASURES_NUMBER = 1000
MSG_TITLE = "msg_"
TRACE_TITLE = "curve_"
N_TITLE = "N.txt"
FILE_FORMAT = ".txt"
DATA_PATH = "./etudiant - " + SET_NUMBER + "/"
E = 2**16 + 1

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

def getN(file) :
    f = open(file, "r")
    N = f.read()
    
    return int(N)

#Opens and reads the chosen file
def open_file(title):
    file = open(title, "r")
    data = []   #table that collects data
    for n in file :
        data = n.split()
    if len(data) == 1:
        data = int(data[0])
    else:
        for i in range(len(data)):
            data[i] = float(data[i])
    return data


def mod_inverse(x,y):

    def eea(a,b):
        if b==0:return (1,0)
        (q,r) = (a//b,a%b)
        (s,t) = eea(b,r)
        return (t, s-(q*t) )

    inv = eea(x,y)[0]
    if inv < 1: inv += y
    return inv