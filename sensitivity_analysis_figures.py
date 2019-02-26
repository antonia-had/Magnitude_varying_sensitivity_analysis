import numpy as np
import matplotlib
from matplotlib import pyplot as plt

# Number of samples in experiment
samples = 1000

# Longform parameter names to use in figure legend
parameter_names_long = ['IWR demand mutliplier', 'Reservoir loss', 
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


# Percentiles for which the sensitivity analysis will be performed
percentiles = np.arange(0,100)
