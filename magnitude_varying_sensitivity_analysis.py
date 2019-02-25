import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import os
from scipy import stats
import pandas as pd

# Number of samples in experiment
samples = 1000 

# Parameter names to use in sensitivity analysis
param_names=['IWRmultiplier','RESloss','TBDmultiplier','M_Imultiplier',
             'Shoshone','ENVflows','EVAdelta','XBM_mu0','XBM_sigma0',
             'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11']

# Longform parameter names to use in figure legend
parameter_names_long = ['IWR demand mutliplier', 'Reservoir loss', 
                        'TBD demand multiplier', 'M&I demand multiplier', 
                        'Shoshone active', 'Env. flow senior right', 
                        'Evaporation delta', 'Dry state mu', 
                        'Dry state sigma', 'Wet state mu', 
                        'Wet state sigma', 'Dry-to-dry state prob.', 
                        'Wet-to-wet state prob.', 'Interaction']

# Percentiles for which the sensitivity analysis will be performed
percentiles = np.arange(0,100)

# Function to calculate custom transparency for legend purposes
def alpha(i, base=0.2):
    l = lambda x: x+base-x*base
    ar = [l(0)]
    for j in range(i):
        ar.append(l(ar[-1]))
    return ar[-1]