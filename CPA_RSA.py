import numpy as np
from utils import *

def M_d_mod_N(M, d, N):
    T = M
    
    for i in range (len(d) - 2, -1, -1):
        T = (T**2)%N    #retrieves the rest of the euclidian division by N
        if(d[i] == 1):
            T = (T*M)%N

def CPA_attack(traces, msg, N):
    hyp_d = [1]   #hypothesis for first bit of d factor : 1
    
    #Initializing tables that contain the Hamming weights for every bit hypothesis
    hamming_weight_for_zeros = np.zeros((MEASURES_NUMBER, 1))
    hamming_weight_for_ones = np.zeros((MEASURES_NUMBER, 1))
    
    

            
if __name__ == "__main__" :
    #do something