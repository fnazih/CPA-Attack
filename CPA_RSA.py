import numpy as np
from utils import *

def M_d_mod_N(M, d, N):
    T = M
    
    for i in range (len(d) - 2, -1, -1):
        T = (T**2)%N    #retrieves the rest of the euclidian division by N
        if(d[i] == 1):
            T = (T*M)%N
