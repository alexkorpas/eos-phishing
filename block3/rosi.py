#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob
from matplotlib.ticker import PercentFormatter
from scipy.stats import norm

#%% Load the data frame

csv_files = glob.glob("../data/*.csv")
dfs = [pd.read_csv(path, sep='","', engine="python") for path in csv_files]
df = pd.concat(dfs, axis=0)
del dfs  # Garbage collection
# df = pd.read_csv("./data/all_phishing_from_1.csv", sep='","', engine="python")

#%% Find annual frequency for a phishing attack
# Drop entries with unknown starting date
df1 = df[df['firsttime'] != '1970-01-01 01:00:00']
df1 = pd.to_datetime(df1["firsttime"])

# Group by year
df2 = df1.groupby(df1.dt.year).count()
df2 = df2.drop(2017)

# Assume that future year will be year will be increased by 500K with a
# deviation of 10% and plot annual frequency
annual_freq_mean = (df2.max() + 500000) * 0.167
annual_freq_std = annual_freq_mean * 0.1
annual_freq = np.random.normal(annual_freq_mean, annual_freq_std, 1000000)
plt.hist(annual_freq, 50, weights=np.ones(len(annual_freq)) / len(annual_freq))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.savefig('fig/annual_freq.png')
plt.clf()


#%% Distribution of the Unitary impact
unit_impact_mean = 900
unit_impact_std = unit_impact_mean * 0.1
unit_impact = np.random.normal(unit_impact_mean, unit_impact_std, 1000000)
plt.hist(unit_impact, 50, weights=np.ones(len(unit_impact)) / len(unit_impact))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.savefig('fig/unit_impact.png')
plt.clf()

#%% Distribution of the Risk exposure
exposure_mean = 327750840
exposure_std = exposure_mean * 0.1
exposure = np.random.normal(exposure_mean, exposure_std, 1000000)
plt.hist(exposure, 50, weights=np.ones(len(exposure)) / len(exposure))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlabel('Risk Exposure (e+8 dollars)')
plt.ylabel('Probability')
plt.savefig('fig/exposure.png')
plt.clf()

#%% Calculate ROSI
cost = 256000
rosi = (exposure * 0.575 - cost) / cost
plt.hist(rosi, 50, weights=np.ones(len(rosi)) / len(rosi))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.xlabel('ROSI')
plt.ylabel('Probability')
plt.savefig('fig/rosi.png')
plt.clf()