#%%
import glob
import pickle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import PercentFormatter
from scipy.stats import norm

#%% Load the data frame

csv_files = glob.glob("../data/*.csv")
dfs = [pd.read_csv(path, sep='","', engine="python") for path in csv_files]
df = pd.concat(dfs, axis=0)
del dfs  # Garbage collection
# df = pd.read_csv("./../data/all_phishing_from_1.csv", sep='","', engine="python")

#%% Compute average uptime over time
# Convert all dates to datetime objects and add them to the DF
# by fixing firsttime and lasttime
max_dt = df['lasttime'].max()
df = df[df['firsttime'] != '1970-01-01 01:00:00']

# Add column "event": 0 if still up, otherwise 1. The "event" is the end of the
# phishing source's uptime.
# df["event"] = 

df.loc[df['lasttime'] < df['firsttime'], 'lasttime'] = max_dt
df["start_dt"] = pd.to_datetime(df["firsttime"])
df["end_dt"] = pd.to_datetime(df["lasttime"])

# Compute useful variables for data processing
earliest_year = min(df.start_dt).year
latest_year = max(df.start_dt).year

# # Unknown lasttimes are indicated as 01-01-1970. We convert these to the date
# # on which the data set was last updated.
final_date = max(df.end_dt)

# Calculate the uptime for each entry and add the uptime column to the df
df["uptime"] = (df["end_dt"] - df["start_dt"]).astype('timedelta64[s]')

# Drop columns that we won't be using for statistical analysis
df = df[['uptime', 'country']]

#%% Merge our processed df with the country IP blacklist data
# Load the CSV that maps countries to amounts of blacklisted IPs
bl_df = pd.read_csv("./../data/blacklist/country-ip-blacklists.csv", sep=",")
bl_df = bl_df[['Country', 'Listings']]  # Only keep relevant columns
bl_df = bl_df.rename(columns={'Country': 'country', 'Listings': 'listings'})

# Merge our phishing attempt df and country blacklist df
merged_df = pd.merge(df, bl_df, on="country")
merged_df = merged_df[merged_df.listings.notnull()]  # Cull NaN-containing rows

# Calculate correlation matrix for the numerical values
analysis_df = merged_df[['uptime', 'listings', 'event']]
corr_mat = analysis_df.corr()
print(corr_mat)

# Create a heatmap for the results
sns.heatmap(corr_mat, annot=True)  # Requires matplotlib version <=3.1.0
plt.tight_layout()
plt.show()
# plt.savefig("./fig/pearson-corr-heatmap.png")
