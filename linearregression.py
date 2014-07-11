#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   1/07/2014


from pandas import Series, DataFrame
from numpy.linalg import inv  

    
def costFnLeastSq( x, y, wgts ):
    """ Implemented the cost function associated with ordinary least square regression
        model """
    p = x.dot( wgts ) #p := pridicted value for y type(p):=pandas.core.series.Series
    diff = p - y[0]   # type(diff) = pandas.core.series.Series; type(y) = DataFrame
    summ = diff.T.dot(diff)
    cost = summ / ( 2.0 * x.index.size )
    return cost
    
def updateWeights( x, y, wgts, rate=0.3 ):
    """Implemention of one iteration of Batch Gradient Descent. 
       Cool thing in this function to notice is that it didn't make use of any 
       for loops. 
       This shows the philosophy of pandas to not use for loops and think in terms 
       of VECTORS """
       
    p = x.dot( wgts )
    diff = y[0] - p
    summ = x.T.dot( diff ) # This step is awesome and shows the power of pandas.
    val = summ * rate
    wgts = wgts + val
    return wgts

def batchGradDes( x, y, rate=0.3 ):
    wgts = Series( 1.0, x.columns )
    diff = 1.0
    cost = costFnLeastSq( x, y, wgts )
    counter = 1
    while diff > 0.0 :
        counter += 1
        wgts = updateWeights( x, y, wgts, rate )
        newcost = costFnLeastSq( x, y, wgts )
        diff = cost - newcost
        cost = newcost
    print "Parameters: \n "
    print wgts
    print "\nTotal iterations: %d" % counter
    print "\nFinal Value of cost function: %f" % cost
    return wgts


def stocGradDes( x, y, rate=0.3, delta=0.1 ):
    wgts = pd.Series( 1.0, x.columns )
    change = 1.0
    cost = costFnLeastSq( x, y, wgts )
    counter = 1
    while change > delta :
        counter += 1
        p = x.dot( wgts )
        diff = y[0] - p
        for i in x.index:
            wgts = wgts + rate * diff[i] * x.loc[i]

        newcost = costFnLeastSq( x, y, wgts )
        change = cost - newcost
        cost = newcost
        if delta < 0.1:             #To make algorithm converge.
            rate = rate - rate * 0.2

    print "Parameters: \n "
    print wgts
    print "\nTotal iterations: %d" % counter
    print "\nFinal Value of cost function: %f" % cost
    return wgts
    
    
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
    
class LinearRegression():
    def __init__(self, fit_intercept=True, normalize=True):
        self.fit_intercept = fit_intercept
        self.normalize = normalize
    
    def fit_SGD(self, x, y, rate=0.3, delta=0.1 ):
        self.coef = stocGradDes(x, y, rate, delta)
        
    def fit_BGD(self, x, y, rate=0.3):
        self.coef = batchGradDes(x, y, rate)
        
    def fit_normalEq(self, x, y):
        self.coef = normalEquation(x, y)
        
    def predict(self, x):
        return x.dot( coef_ )
    
    def error(x, y)       
        pre_y = self.predict( x )
        diff = y - pre_y
        errorval = pow(diff, 2).sum()/y.size 
        return errorval
        
    def cost_fn_value(x,y,wgts=self.coef):
        return costFnLeastSq(x,y,wgts)
         
        
    
        
    
