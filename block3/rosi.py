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
mu = df2.max() + 500000
variance = mu * 0.1
values = np.random.normal(mu, variance, 1000000)
plt.hist(values, 50, weights=np.ones(len(values)) / len(values))
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.savefig('fig/annual_freq.png')
plt.clf()


