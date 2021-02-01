import numpy as np
from math import gcd, sqrt

SET_NUMBER = "10"
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

#Retrieves the N data from "N.txt" file
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
    file.close()
    return data

#Retrieves the modular inverse using the Extended Euclidian Algorithm
def mod_inverse(x,y):

    def eea(a,b):
        if b==0:return (1,0)
        (q,r) = (a//b,a%b)
        (s,t) = eea(b,r)
        return (t, s-(q*t) )

    inv = eea(x,y)[0]
    if inv < 1: inv += y
    return inv

#Montgomery multiplication implementation
def M_d_mod_N(M, d, N):
    T = M
    h_weight = 0
    
    for i in range (len(d) - 2, -1, -1):
        T = (T**2)%N    #retrieves the rest of the euclidian division by N
        if(d[i] == 1):
            T = (T*M)%N
            if i == 0:
                h_weight = hamming_weight(T)
        else:
            if(i == 0):
                T = (T**2)%N
                h_weight = hamming_weight(T)
                
    return h_weight

def CPA_attack(data, N) :
    hyp_d = [1]   #hypothesis for first bit of d factor : 1
    
    #Initializing tables that contain the Hamming weights for every bit hypothesis
    hamming_weight_for_zeros = np.zeros((MEASURES_NUMBER, 1))
    hamming_weight_for_ones = np.zeros((MEASURES_NUMBER, 1))
    
    mat_coeff_corr_finale = []
    
    counter = 2
    
    while(data[0][counter] != -1000):   #while consumption data is still relevant
        for i in range(MEASURES_NUMBER):   #for every message
            #Hypothesis : bit is set
            temp_d = [0] + hyp_d
            hamming_weight_for_zeros[i] = M_d_mod_N(data[i][0], temp_d, N)
            #Hypothesis : bit is unset
            temp_d = [1] + hyp_d
            hamming_weight_for_ones[i] = M_d_mod_N(data[i][0], temp_d, N)
        
        temp_data = []    #formatting for corrcoeff function
        for i in range(MEASURES_NUMBER) :
            temp_data.append(data[i][counter:counter + 1])
        
        mat_corr_zeros = np.corrcoef(temp_data, hamming_weight_for_zeros, False)
        mat_corr_ones = np.corrcoef(temp_data, hamming_weight_for_ones, False)
        
        coeff_corr_one = mat_corr_ones[1][0]
        coeff_corr_zero = mat_corr_zeros[1][0]
        
        if(coeff_corr_zero >= coeff_corr_one) :   #if unset bit is more likely
            hyp_d = [0] + hyp_d
            counter += 1   #only one operation made
            mat_coeff_corr_finale.append(coeff_corr_zero)
        else :
            hyp_d = [1] + hyp_d
            counter += 2   #two operations made
            mat_coeff_corr_finale.append(coeff_corr_one)
            
    hyp_d.reverse()
    return hyp_d, mat_coeff_corr_finale

#attack on RSA by factoring N
def factorisation(e, n) :
    p, q = find_prime_factors(n)
    
    phi_n = (p - 1)*(q - 1)
    real_d = mod_inverse(e, phi_n)
    
    return real_d
    

#importing data from files    
data = MEASURES_NUMBER*[[]]
for i in range(MEASURES_NUMBER) :
         title = DATA_PATH + MSG_TITLE + str(i) + FILE_FORMAT
         msg = open_file(title)
         data[i] = [msg]
         title = DATA_PATH + TRACE_TITLE + str(i) + FILE_FORMAT
         trace = open_file(title)
         data[i] = data[i] + trace
            
N = getN(DATA_PATH + N_TITLE)   #importing N
d, coeff_final = CPA_attack(data, N)   #performing CPA attack
print("Correlation coefficients for every bit with CPA attack")
print(coeff_final)

d_str = ""
for bit in d :
    d_str += str(bit)
print("Key found by CPA attack : 0b" + d_str)

real_d = factorisation(E, N)   #performing attack by factoring
print("Key found by factoring : " + bin(real_d))

print("Writing key in file...")
file = open("d_10.txt", "w")
for bit in d :
    file.write(str(bit))
file.close()

print("Writing done")