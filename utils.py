import numpy as np
from matplotlib import pyplot as plt
from math import *

SET_NUMBER = ""
KEY_SIZE = 32
MEASURES_NUMBER = 999
MSG_TITLE = "msg_"
TRACE_TITLE = "curve_"
FILE_FORMAT = ".txt"
DATA_PATH = "./EMSE/Etudiant - " + SET_NUMBER + "/"

#Calculates the Hamming weight of the parameter, i.e. the number of '1' in binary
def hamming_weight(x):    
    return bin(x).count("1")

#Opens and reads the chosen file
def open_files(title, size):
    

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

def openFile(title, size) :
    file = open(title, "r")
    data = []   #table that collects data
    
    for i in range(size) :
        