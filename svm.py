#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   16/07/2014

import pandas as pd
import numpy as np

"""
    alpha's is a DataFrame with one row namely 'val'(which gives the value of alpha   
    at index=pos). Index is saved as columns names.
    In SVM as most of alpha's will be zero so there is no point in storing them.
    We just need to know the position and value of non-zero alphaS's
"""


class Alpha():
    def __init__( self, index=None, val=None ):
        self.alpha = pd.DataFrame(0.0,index=['val'], columns=[])
        
    def add( self, index, val ):
        self.alpha[index] = val
        
    def value( self, i ):
        value = self.alpha.columns[alphas.columns==i]#Searching for a value in columns
                                                     #of alpha
        if value.size == 0:
            return 0
        return self.alpha[value[0]]
        
    def size( self ):
        return self.alpha.columns.size
        
    def indexValue( self ):
        return self.alpha.columns


def fx( x, y, alphas, b, sample ):
    total = 0.0
    for i in alphas.columns:
        total = total + alphas.value(i) * y[i] * kernal(x[i], sample)
    total = total + b
    return total

def bounds( y, alphas, i, j, C ):
    if y[i] != y[j]:
        L = max( 0.0, alphas.value(i) - alphas.value(j) )
        H = min( C, C + alphas.value(i) + alphas.value(j) )
    else:
        L = max( 0.0, alphas.value(i) + alphas.value(j) - C )
        H = min( C, alphas.value(i) + alphas.value(j) )
    
    return { 'L':L, 'H':H }
    
def svm( x, y, tol, C, max_passes ):
    alphas = Alpha()
    b = 0.0
    passes = 0
    while( passes < max_passes ):
        num_changed_alphas = 0
        for i in x.columns.size:
            Ei = fx( x, y, alphas, b, x[i] ) - y[i]
            if ( y[i] * Ei < -tol and alphas.value(i) < C ) or 
               ( y[i] * Ei > tol and alphas.value(i) > 0 ):
                Select j != i
                Ej = fx( x, y, alphas, b, x[j] ) - y[j]
                aiold = alphas.value(i)
                ajold = alphas.value(j)
                LHbounds = bounds( y, alphas, i, j, C )
                L = LHbounds['L']
                H = LHbounds['H']
                if L == H:
                    continue
                neta = 2*kernal(x[i], x[j]) - kernal(x[i], x[i]) - kernal(x[j], x[j])
                if ( neta >= 0 ):
                    continue
                ajnew = ajold - ( y[j] * ( Ei -Ej ) / neta )
                if ajnew > H:
                    ajnew = H
                elif ajnew < L:
                    ajnew = L
                #one step missing
                ainew = aiold + y[i] * y[j] * ( ajold - ajnew )
                
                alphas.add( i, ainew )
                alphas.add( j, ajnew )
                
                b1 = b - Ei - y[i] * ( ainew - aiold ) * kernal(x[i], x[i]) - y[j] * 
                      (ajnew - ajold) * kernal(x[i],x[j])
                b2 = b - Ej - y[i] * ( ainew - aiold ) * kernal(x[i], x[j]) - y[j] * 
                      (ajnew - ajold) * kernal(x[j],x[j])
                      
                if 0 < ainew and ainew < C:
                    b = b1
                elif 0 < ajnew and ajnew < C:
                    b = b2
                else:
                    b = (b1 + b2) / 2
                    
                num_changed_alphas = num_changed_alphas + 1
                
        if num_changed_alphas == 0:
            passes = passes + 1
        else:
            passes = 0
            
            
            
