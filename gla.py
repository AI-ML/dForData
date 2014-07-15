#   Author: Salil Agarwal (salil@dfordata.com)
#   Date:   5/07/2014

import pandas as pd
import numpy as np


def calParameters(x,y):
    parameters = {}
    yfreq = y.value_counts()
    yprob = yfreq / y.size
    parameters['y'] = yprob #yprob = probability of y (prior)
    x['y'] = y
    xsorted = x.sort_index(by=['y'])
    xsorted.index = range(0,y.size)
    del xsorted['y']
    j = 0
    counter = 0
    means = pd.Series(0.0)
    for i in yfreq:
        xpart = pd.DataFrame( xsorted[j:i+j] )
        means[yfreq.index[counter]] = xpart.mean()
        j = i + j
        counter += 1
    parameters['mean'] = means
    if pd.Series(x.values.ravel()).unique().size > 2: # calculating covariance matrix
        
        # covariance matrix for a 10 features x will be a 10X10 matrix 
        cov = pd.DataFrame( 0, index=x.columns, columns=x.columns )
        for i in x.index:
            cov = cov + (x.loc[i] - means[y[i]]).dot((x.loc[i] - means[y[i]]).T)
        para['covariance'] = cov
    return para
    
    
class GDAClassification():
    def __init__( self, normalize=True ):
        self.normalize = normalize
        
    def fit( self, x, y ):
        parameters = calParameters( x, y )
        self.prior = parameters['y']
        self.means = parameters['mean']
        if parameters.has_key('covariance'):
            self.covariance = parameters['covariance']
            self.covinv = pd.DataFrame(np.linalg.inv(self.covarinace))
        
    def predict( self, x=pd.Series(0) ):
    """ Predicts the class of given x. Notice that here x is a series, so only one 
        example can be classified at a time"""
        constant = 1 / ( pow(2*np.pi, x.size/2) * pow(np.linalg(self.covariance.as_matrix()), 0.5) )
        
        pxgiveny = pd.Series(0.0)
        for i in self.means.index:
            pxgiveny[i] = constant* np.exp( -0.5 * ((x - self.means[i]).dot(self.covinv).dot(x - self.means[i])) )
        
        pxy = pxgiveny * self.prior
        px = pxy.sum()
        self.posterior = pxy / px
        return self.posterior.idxmax()
        
    def error( self, x, y ):
        wrong = 0
        for i in x.index:
            pre_y = self.predict( x.loc(i) )
            if pre_y != y[i]:
                wrong++
        return wrong / y.size
 
 class NaiveBayes():
    def __init__( self, normalize=True ):
        self.normalize = normalize
    
    def fit( self, x, y ):
        parameters = calParameters( x, y )
        self.prior = parameters['y']
        self.px_given_y = parameters['mean']
    def predict( self, x ):
        for i in x.index:
            
        
