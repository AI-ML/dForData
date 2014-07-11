#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   3/07/2014

from math import exp
from pandas import Series, DataFrame
import numpy as np
from linearregression import LinearModel

def costFn( x, y, wgts ):
    """ Implemented the cost function associated with logistic regression algorithm """
    p = 1 / ( 1 + np.exp(-x.dot(wgts)) ) 
    #p := pridicted value for y type(p):=pandas.core.series.Series
    summ = y.T.dot( np.log(p) ) + (1 - y).T.dot( np.log(1 - p) )
    return summ


def stocGradDes( x, y, rate=0.3, delta=0.1 ):
    wgts = Series( 1.0, x.columns )
    change = 1.0
    cost = costFn( x, y, wgts )
    counter = 1
    while change > delta :
        counter += 1
        p = 1 / ( 1 + np.exp(-x.dot(wgts)) ) 
        diff = y[0] - p
        for i in x.index:
            wgts = wgts + rate * diff[i] * x.loc[i]

        newcost = costFn( x, y, wgts )
        change = newcost - cost
        cost = newcost
        if delta < 0.1:             #To make algorithm converge.
            rate = rate - rate * 0.2

    print "Parameters: \n "
    print wgts
    print "\nTotal iterations: %d" % counter
    print "\nFinal Value of cost function: %f" % cost
    return wgts
    
    
class LogisticRegression(LinearModel):

    def fit_SGD(self, x, y, rate=0.3, delta=0.1 ):
        self.coef = stocGradDes(x, y, rate, delta)
    
    def predict(self, x):
        p = 1 / ( 1 + np.exp(-x.dot(self.coef)) ) 
        return p
    
    def error(self, x, y):    
        pre_y = self.predict( x )
        diff = y - pre_y
        errorval = pow(diff,2).sum()/y.size
        return errorval
        
    def cost_fn_value(self, x, y, wgts=None):
        if wgts is None:
            wgts = self.coef
        return costFn(x,y,wgts)
    
    
    
