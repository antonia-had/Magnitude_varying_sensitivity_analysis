import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import pandas as pd

# Number of samples in experiment
LHsamples = np.loadtxt('./LHsamples.txt') 
samples = len(LHsamples[1,:])

# Parameter names for figure generation
param_names=['IWRmultiplier','RESloss','TBDmultiplier','M_Imultiplier',
             'Shoshone','ENVflows','EVAdelta','XBM_mu0','XBM_sigma0',
             'XBM_mu1','XBM_sigma1','XBM_p00','XBM_p11']

# Longform parameter names to use in figure legend
parameter_names_long = ['Min','IWR demand mutliplier', 'Reservoir loss', 
                        'TBD demand multiplier', 'M&I demand multiplier', 
                        'Shoshone active', 'Env. flow senior right', 
                        'Evaporation delta', 'Dry state mu', 
                        'Dry state sigma', 'Wet state mu', 
                        'Wet state sigma', 'Dry-to-dry state prob.', 
                        'Wet-to-wet state prob.', 'Interaction']

# Read in historical data
histData = np.loadtxt('./historical_data.txt')

# Plot historical series
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(np.arange(len(histData)),histData, c='black')
ax.set_ylabel('Annual shortage (af)', fontsize=12)
ax.set_xlabel('Year on record', fontsize = 12)
plt.savefig('historical_data.png')

# Sort historical data in percentiles of magnitude
hist_sort = np.sort(histData)

# Estimate percentiles according to record length
P = np.arange(1.,len(histData)+1)*100 / len(histData)

# Plot historical percentiles of magnitude
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
ax.plot(P,hist_sort, c='black')
ax.set_ylabel('Annual shortage (af)', fontsize=12)
ax.set_xlabel('Shortage magnitude percentile', fontsize=12)
plt.savefig('historical_data_percentiles.png')

# Read in experiment data
expData = np.loadtxt('./experiment_data.txt')

# Sort experiment data in percentiles of magnitude
expData_sort = np.zeros_like(expData)
for j in range(samples):
    expData_sort[:,j] = np.sort(expData[:,j])
    

# Plot historical percentiles of magnitude and sampled series        
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
for j in range(samples):
    ax.plot(P,expData_sort[:,j], c = '#4286f4')
ax.plot(P,expData_sort[:,0], c = '#4286f4', label = 'Experiment')            
ax.plot(P,hist_sort, c='black', label = 'Historical')
ax.legend(loc = 'upper left')
ax.set_ylabel('Annual shortage (af)', fontsize=12)
ax.set_xlabel('Shortage magnitude percentile', fontsize=12)
plt.savefig('experiment_data_all.png') 

# Plot range of experiment outputs
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
ax.fill_between(P, np.min(expData_sort[:,:],1), np.max(expData_sort[:,:], 1), color='#4286f4', alpha = 0.1, label = 'Experiment')
ax.plot(P, np.min(expData_sort[:,:],1), linewidth=0.5, color='#4286f4', alpha = 0.3)
ax.plot(P, np.max(expData_sort[:,:],1), linewidth=0.5, color='#4286f4', alpha = 0.3)        
ax.plot(P,hist_sort, c='black', label = 'Historical')
ax.legend(loc = 'upper left')
ax.set_ylabel('Annual shortage (af)', fontsize=12)
ax.set_xlabel('Shortage magnitude percentile', fontsize=12)
plt.savefig('experiment_data_range.png') 

# To plot output density of experiment we need an array of percentiles
p=np.arange(100,0,-10)

# Function to calculate custom transparency for legend purposes
def alpha(i, base=0.2):
    l = lambda x: x+base-x*base
    ar = [l(0)]
    for j in range(i):
        ar.append(l(ar[-1]))
    return ar[-1]

handles = []
labels=[]
fig = plt.figure()
ax=fig.add_subplot(1,1,1)
for i in range(len(p)):
    ax.fill_between(P, np.min(expData_sort[:,:],1), np.percentile(expData_sort[:,:], p[i], axis=1), color='#4286f4', alpha = 0.1)
    ax.plot(P, np.percentile(expData_sort[:,:], p[i], axis=1), linewidth=0.5, color='#4286f4', alpha = 0.3)
    handle = matplotlib.patches.Rectangle((0,0),1,1, color='#4286f4', alpha=alpha(i, base=0.1))
    handles.append(handle)
    label = "{:.0f} %".format(100-p[i])
    labels.append(label)
ax.plot(P,hist_sort, c='black', linewidth=2, label='Historical record')
ax.set_xlim(0,100)
ax.legend(handles=handles, labels=labels, framealpha=1, fontsize=8, loc='upper left', title='Frequency in experiment',ncol=2)
ax.set_xlabel('Shortage magnitude percentile', fontsize=12)
plt.savefig('experiment_data_density.png')

# Percentiles for analysis to loop over
percentiles = np.arange(0,100)

# Estimate upper and lower bounds
globalmax = [np.percentile(np.max(expData_sort[:,:],1),p) for p in percentiles]
globalmin = [np.percentile(np.min(expData_sort[:,:],1),p) for p in percentiles]

delta_values = pd.read_csv('./DELTA_scores.csv')
delta_values.set_index(list(delta_values)[0],inplace=True)
delta_values = delta_values.clip(lower=0)
bottom_row = pd.DataFrame(data=np.array([np.zeros(100)]), index= ['Interaction'], columns=list(delta_values.columns.values))
top_row = pd.DataFrame(data=np.array([globalmin]), index= ['Min'], columns=list(delta_values.columns.values))
delta_values = pd.concat([top_row,delta_values.loc[:],bottom_row])
for p in range(len(percentiles)):
    total = np.sum(delta_values[str(percentiles[p])])-delta_values.at['Min',str(percentiles[p])]
    if total!=0:
        for param in param_names:
                value = (globalmax[p]-globalmin[p])*delta_values.at[param,str(percentiles[p])]/total
                delta_values.set_value(param,str(percentiles[p]),value)
delta_values = delta_values.round(decimals = 2)
delta_values_to_plot = delta_values.values.tolist()

S1_values = pd.read_csv('./S1_scores.csv')
S1_values.set_index(list(S1_values)[0],inplace=True)
S1_values = S1_values.clip(lower=0)
bottom_row = pd.DataFrame(data=np.array([np.zeros(100)]), index= ['Interaction'], columns=list(S1_values.columns.values))
top_row = pd.DataFrame(data=np.array([globalmin]), index= ['Min'], columns=list(S1_values.columns.values))
S1_values = pd.concat([top_row,S1_values.loc[:],bottom_row])
for p in range(len(percentiles)):
    total = np.sum(S1_values[str(percentiles[p])])-S1_values.at['Min',str(percentiles[p])]
    if total!=0:
        diff = 1-total
        S1_values.set_value('Interaction',str(percentiles[p]),diff)
        for param in param_names+['Interaction']:
            value = (globalmax[p]-globalmin[p])*S1_values.at[param,str(percentiles[p])]/total
            S1_values.set_value(param,str(percentiles[p]),value)
S1_values = S1_values.round(decimals = 2)
S1_values_to_plot = S1_values.values.tolist()

R2_values = pd.read_csv('./R2_scores.csv')
R2_values.set_index(list(R2_values)[0],inplace=True)
R2_values = R2_values.clip(lower=0)
bottom_row = pd.DataFrame(data=np.array([np.zeros(100)]), index= ['Interaction'], columns=list(R2_values.columns.values))
top_row = pd.DataFrame(data=np.array([globalmin]), index= ['Min'], columns=list(R2_values.columns.values))
R2_values = pd.concat([top_row,R2_values.ix[:],bottom_row])
for p in range(len(percentiles)):
    total = np.sum(R2_values[str(percentiles[p])])-R2_values.at['Min',str(percentiles[p])]
    if total!=0:
        value = 1-total
        R2_values.set_value('Interaction',str(percentiles[p]),value)
    R2_values[str(p)]=(globalmax[p]-globalmin[p])*R2_values[str(percentiles[p])]
R2_values = R2_values.round(decimals = 2)
R2_values_to_plot = R2_values.values.tolist()

color_list = ["white", "#F18670", "#E24D3F", "#CF233E", "#681E33", "#676572", "#F3BE22", "#59DEBA", "#14015C", "#DAF8A3", "#0B7A0A", "#F8FFA2", "#578DC0", "#4E4AD8", "#F77632"]        

fig, (ax1, ax2, ax3) = plt.subplots(1,3, figsize=(14.5,8))
ax1.stackplot(percentiles, delta_values_to_plot, colors = color_list, labels=parameter_names_long)
l1 = ax1.plot(percentiles, globalmax, color='black', linewidth=2)
l2 = ax1.plot(percentiles, globalmin, color='black', linewidth=2)
ax1.set_title("Delta index")
ax1.set_xlim(0,100)
ax2.stackplot(np.arange(0,100), S1_values_to_plot, colors = color_list, labels=parameter_names_long)
ax2.plot(percentiles, globalmax, color='black', linewidth=2)
ax2.plot(percentiles, globalmin, color='black', linewidth=2)
ax2.set_title("S1")
ax2.set_xlim(0,100)
ax3.stackplot(np.arange(0,100), R2_values_to_plot, colors = color_list, labels=parameter_names_long)
ax3.plot(percentiles, globalmax, color='black', linewidth=2)
ax3.plot(percentiles, globalmin, color='black', linewidth=2)
ax3.set_title("R^2")
ax3.set_xlim(0,100)
handles, labels = ax3.get_legend_handles_labels()
ax1.set_ylabel('Annual shortage (af)', fontsize=12)
ax2.set_xlabel('Shortage magnitude percentile', fontsize=12)
ax1.legend((l1), ('Global ensemble',), fontsize=10, loc='upper left')
fig.legend(handles, labels, fontsize=10, loc='lower center',ncol = 5)
plt.subplots_adjust(bottom=0.2)
fig.savefig('./experiment_sensitivity_curves.png')
