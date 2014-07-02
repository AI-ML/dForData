#   Date: 1/07/2014
#   Name: Salil Agarwal

import pandas as pd

"""def schoLR( X=pd.DataFrame(), Y=pd.Series(), theta=pd.Series(1.0, index=[0,1]), rate=0.3 ):
    #Checking sizes of theta and X.columns
    if theta.size + 1 != X.columns.size:
        theta = pd.Series(1.0, index=range(X.columns.size + 1)
    
    for i in range(X.index.size):
        h_theta = thetaTX( X.loc[i], theta ) 
        for j in range(theta.index.size):
            theta[j] = theta[j] + rate * ( Y[i] - h_theta) ) * X[j][i]
    return theta   

def thetaTX( X=pd.Series(), theta=pd.Series() ):
    sum = 0.0
    for i in range(X.size):
        sum = sum + X[i]*theta[i]
    return sum"""
    
    
def costFnLeastSq( x, y, wgts ):
    """ Implemented the cost function associated with ordinary least square regression
        model J()"""
    p = x.dot( wgts ) #p := pridicted value for y type(p):=pandas.core.series.Series
    diff = p - y[0]   # type(diff) = pandas.core.series.Series; type(y) = DataFrame
    diffsq = pow( diff, 2 )
    summ = diffsq.sum()
    error = summ / ( 2.0 * x.index.size )
    return error
    
def updateWeights( x, y, wgts ):
    """Implemention of one iteration of Batch Gradient Descent. 
       Cool thing in this function to notice is that it didn't make use of any 
       for loops. 
       This shows the philosophy of pandas to not use for loops and think in terms 
       of VECTORS """
       
    rate = 0.3
    p = x.dot( wgts )
    diff = y[0] - p
    summ = x.T.dot( diff ) # This step is awesome and shows the power of pandas.
    val = summ * rate
    wgts = wgts + val
    return wgts

def batchGradDes( x, y ):
    wgts = pd.Series( 1.0, x.columns )
    diff = 1.0
    cost = costFnLeastSq( x, y, wgts )
    print ( "%f \n" %diff )
    counter = 1
    while diff > 0.0 :
        counter += 1
        wgts = updateWeights( x, y, wgts )
        newcost = costFnLeastSq( x, y, wgts )
        print ( "%f \n" %diff )
        diff = cost - newcost
        cost = newcost
    print wgts
    print counter
    print "\n"
    print cost
    return wgts


    
    
