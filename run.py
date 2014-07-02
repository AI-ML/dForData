#   Author: Salil Agarwal
#   Date: 2/07/2014

import pandas as pd
from sklearn import datasets
import linearmodel

diabetes = datasets.load_diabetes() #diabetes is a Scikit object
x = pd.DataFrame( diabetes.data ) # diabetes.data gives feature data
y = pd.DataFrame( diabetes.target ) # diabetes.target gives label data

wgts = linearmodel.batchGradDes(x,y)

