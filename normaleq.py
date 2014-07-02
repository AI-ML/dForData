#   Author: Salil Agarwal
#   Date:   2/07/2014

# Normal Equation 

from numpy.linalg import inv
from pandas import DataFrame

def normalEquation( x, y ):
    """ Calculate weights for linear regression directly using Normal Equation
        method"""
    xTx = x.T.dot(x)
    matrix_form = xTx.as_matrix()
    inverse = inv( matrix_form )
    #back to dataframe 
    inverse = DataFrame( inverse )
    weights = inverse.dot(x.T).dot(y)
    return weights[0]
