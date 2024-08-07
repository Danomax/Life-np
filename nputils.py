import numpy as np

def repeat_n(arr,n):
    '''
    util para pasar una matriz de valores
    a un color de n valores (n = 3 o 4)
    '''
    return np.repeat(arr,n).reshape((arr.shape[0],arr.shape[1],n))