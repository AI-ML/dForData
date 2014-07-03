#   Author: Salil Agarwal
#   Date:   3/07/2014

from pandas import DataFrame

def midSliceOfData(x, fraction=0.7):
    """ Returns a new copy of data with its own indexing(0...n-1)"""
    size = x.index.size
    lowerbound = int( size * ((1-fraction)/2) )
    upperbound = size - lowerbound
    dataslice = DataFrame( x[lowerbound:upperbound] )
    dataslice.index = range( 0, upperbound-lowerbound )
    return dataslice
    
def boundingData( x, fraction=0.3 ):
    size = x.index.size
    lowerbound = int( size * ((fraction)/2) )
    upperbound = size - lowerbound
    bounddata = DataFrame( x[0:lowerbound] )
    bounddata = bounddata.append( x[upperbound:size] )
    bounddata.index = range( 0, lowerbound + size - upperbound )
    return bounddata
    
    
    
    
    
    
