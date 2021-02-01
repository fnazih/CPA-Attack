import numpy as np
from utils import *
from math import gcd

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
    
    while(data[0][counter] != -1000):
        for i in range(MEASURES_NUMBER):
            #Hypothesis : bit is set
            temp_d = [0] + hyp_d
            hamming_weight_for_zeros[i] = M_d_mod_N(data[i][0], temp_d, N)
            #Hypothesis : bit is unset
            temp_d = [1] + hyp_d
            hamming_weight_for_ones[i] = M_d_mod_N(data[i][0], temp_d, N)
        
        temp_data = []
        for i in range(MEASURES_NUMBER) :
            temp_data.append(data[i][counter:counter + 1])
        
        mat_corr_zeros = np.corrcoef(temp_data, hamming_weight_for_zeros, False)
        mat_corr_ones = np.corrcoef(temp_data, hamming_weight_for_ones, False)
        
        coeff_corr_one = mat_corr_ones[1][0]
        coeff_corr_zero = mat_corr_zeros[1][0]
        
        if(coeff_corr_zero >= coeff_corr_one) :
            hyp_d = [0] + hyp_d
            counter += 1
            mat_coeff_corr_finale.append(coeff_corr_zero)
        else :
            hyp_d = [1] + hyp_d
            counter += 2
            mat_coeff_corr_finale.append(coeff_corr_one)
            
    hyp_d.reverse()
    return hyp_d, mat_coeff_corr_finale

def factorisation(e, n) :
    p, q = find_prime_factors(n)
    
    phi_n = (p - 1)*(q - 1)
    real_d = mod_inverse(e, phi_n)
    
    return real_d
    
data = MEASURES_NUMBER*[[]]

for i in range(MEASURES_NUMBER) :
         title = DATA_PATH + MSG_TITLE + str(i) + FILE_FORMAT
         msg = open_file(title)
         data[i] = [msg]
         title = DATA_PATH + TRACE_TITLE + str(i) + FILE_FORMAT
         trace = open_file(title)
         data[i] = data[i] + trace
            

N = getN(DATA_PATH + N_TITLE)
d, coeff_final = CPA_attack(data, N)
d_str = ""

for bit in d :
    d_str += str(bit)
print("0b" + d_str)

real_d = factorisation(E, N)
print(bin(real_d))


