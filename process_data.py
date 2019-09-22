#%%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

from collections import defaultdict, OrderedDict

# %% Load the data frame
csv_files = glob.glob("./data/*.csv")
dfs = [pd.read_csv(path, sep='","', engine="python") for path in csv_files]
df = pd.concat(dfs, axis=0)
del dfs  # Garbage collection
# df = pd.read_csv("./data/all_phishing_from_1.csv", sep='","', engine="python")

#%% Compute occurrence counts
for attribute in ["ip", "country", "domain", "email"]:
    occurrence_counts = df[attribute].value_counts().head(10)
    # Plot the top 10 occurrence counts
    occurrence_counts.plot.bar()
    plt.title(f"Top 10 {attribute} occurrence counts")
    plt.tight_layout()
    # plt.savefig(f"./fig/{attribute}-occurrence-counts.png")
    # plt.show()
    plt.clf()

#%% Compute average uptime over time
# Convert all dates to datetime objects and add them to the DF
# by fixing firsttime and lasttime
max_dt = df['lasttime'].max()
df = df[df['firsttime'] != '1970-01-01 01:00:00']
df.loc[df['lasttime'] < df['firsttime']] = max_dt
df["start_dt"] = pd.to_datetime(df["firsttime"])
df["end_dt"] = pd.to_datetime(df["lasttime"])

# Calculate the uptime for each entry, group them by month and find average
df1 = df[["start_dt", "end_dt"]]
df1["uptime"] = (df1["end_dt"] - df1["start_dt"]).astype('timedelta64[s]')
df1 = df1.drop("end_dt", axis=1)
df2 = df1.groupby(df1["start_dt"].dt.to_period("M")).mean()

# Plot the results
df2.plot()
plt.title(f"Average uptime over time")
plt.ylabel("Uptime (seconds)")
plt.xlabel("Date")
plt.tight_layout()
plt.savefig("fig/uptime-vs-date.png")
plt.clf()

#%% Compute the percentage of phishing attacks hosted on HTTPS per year
