import numpy as np
import pandas as pd
import statsmodels.api as sm
import scipy.stats
import matplotlib.pyplot as plt 
from SALib.analyze import delta

LHsamples = np.loadtxt('./LHsamples.txt') 
params_no = len(LHsamples[0,:])