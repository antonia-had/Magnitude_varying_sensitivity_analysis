import numpy as np
import pandas as pd
import statsmodels.api as sm
from SALib.analyze import delta

# Load parameter samples
LHsamples = np.loadtxt('./LHsamples.txt') 
params_no = len(LHsamples[0,:])
param_bounds=np.loadtxt('./uncertain_params.txt', usecols=(1,2))

# Parameter names
param_names=['IWRmultiplier','RESloss','TBDmultiplier','M_Imultiplier',
             'Shoshone','ENVflows','EVAdelta','XBM_mu0','XBM_sigma0',
             'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11']

# Define problem class
problem = {
    'num_vars': params_no,
    'names': param_names,
    'bounds': param_bounds.tolist()
}

# Percentiles for analysis to loop over
percentiles = np.arange(0,100)

# Function to fit regression with Ordinary Least Squares using statsmodels
def fitOLS(dta, predictors):
    # concatenate intercept column of 1s
    dta['Intercept'] = np.ones(np.shape(dta)[0]) 
    # get columns of predictors
    cols = dta.columns.tolist()[-1:] + predictors 
    #fit OLS regression
    ols = sm.OLS(dta['Shortage'], dta[cols])
    result = ols.fit() 
    return result 

# Create empty dataframes to store results
DELTA = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
DELTA_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
S1 = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
S1_conf = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
R2_scores = pd.DataFrame(np.zeros((params_no, len(percentiles))), columns = percentiles)
DELTA.index=DELTA_conf.index=S1.index=S1_conf.index = R2_scores.index = param_names

# Read in experiment data
expData = np.loadtxt('./experiment_data.txt')

# Identify magnitude at each percentiles
syn_magnitude = np.zeros([len(percentiles),len(LHsamples[:,0])])
for j in range(len(LHsamples[:,0])):
    syn_magnitude[:,j]=[np.percentile(expData[:,j], i) for i in percentiles]

# Delta Method analysis
for i in range(len(percentiles)):
    if syn_magnitude[i,:].any():
        try:
            result= delta.analyze(problem, LHsamples, syn_magnitude[i,:], print_to_console=False, num_resamples=2)
            DELTA[percentiles[i]]= result['delta']
            DELTA_conf[percentiles[i]] = result['delta_conf']
            S1[percentiles[i]]=result['S1']
            S1_conf[percentiles[i]]=result['S1_conf']
        except:
            pass

S1.to_csv('./S1_scores.csv')
S1_conf.to_csv('./S1_conf_scores.csv')
DELTA.to_csv('./DELTA_scores.csv')
DELTA_conf.to_csv('./DELTA_conf_scores.csv')

# OLS regression analysis
dta = pd.DataFrame(data = LHsamples, columns=param_names)
#    fig = plt.figure()
for i in range(len(percentiles)):
    shortage = np.zeros(len(LHsamples[:,0]))
    for k in range(len(LHsamples[:,0])):
            shortage[k]=syn_magnitude[i,k]
    dta['Shortage']=shortage
    for m in range(params_no):
        predictors = dta.columns.tolist()[m:(m+1)]
        result = fitOLS(dta, predictors)
        R2_scores.at[param_names[m],percentiles[i]]=result.rsquared    
R2_scores.to_csv('./R2_scores.csv')