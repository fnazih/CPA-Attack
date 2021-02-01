import numpy as np
from utils import *
from math import gcd

def M_d_mod_N(M, d, N):
    T = M
    hamming_weight = 0
    
    for i in range (len(d) - 2, -1, -1):
        T = (T**2)%N    #retrieves the rest of the euclidian division by N
        if(d[i] == 1):
            T = (T*M)%N
            if i == 0:
                hamming_weight = hamming_weight(T)
        else:
            if(i == 0):
                T = (T**2)%N
                hamming_weight = hamming_weight(T)
                
    return hamming_weight

def concatenate_msgs() :
    all_msgs = []
    
    for i in range(MEASURES_NUMBER) :
        title = DATA_PATH + MSG_TITLE + i + FILE_FORMAT
        msg = open_file(title)
        all_msgs.append(msg)
        
    return all_msgs


def CPA_attack(traces, msg, N):
    hyp_d = [1]   #hypothesis for first bit of d factor : 1
    
    #Initializing tables that contain the Hamming weights for every bit hypothesis
    hamming_weight_for_zeros = np.zeros((MEASURES_NUMBER, 1))
    hamming_weight_for_ones = np.zeros((MEASURES_NUMBER, 1))
    
    counter = 0
    
    while(traces[0][counter] != -1000):
        for i in range(MEASURES_NUMBER):
            #Hypothesis : bit is set
            temp_d = [0] + hyp_d
            hamming_weight_for_zeros[i] = M_d_mod_N(msg[i], temp_d, N)
            #Hypothesis : bit is unset
            temp_d = [1] + hyp_d
            hamming_weight_for_ones[i] = M_d_mod_N(msg[i], temp_d, N)
        
        mat_corr_zeros = np.corrcoef(hamming_weight_for_zeros, traces[:, counter:counter + 1], False)
        mat_corr_ones = np.corrcoef(hamming_weight_for_ones, traces[:, counter:counter + 1], False)
        
        if(mat_corr_zeros > mat_corr_ones) :
            hyp_d = [0] + hyp_d
        else :
            hyp_d = [1] + hyp_d
            
#if __name__ == "__main__" :
    #do something