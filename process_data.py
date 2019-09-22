import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

from collections import defaultdict

# Load the data frame
# csv_files = glob.glob("./data/*.csv")
# dfs = [pd.read_csv(path, sep='","', engine="python") for path in csv_files]
# # df = pd.read_csv("./data/all_phishing_from_1.csv", sep='","', engine="python")
# df = pd.concat(dfs, axis=0)
# del dfs  # Garbage collection

df = pd.read_csv("./data/all_phishing_from_1.csv", sep='","', engine="python")

# Compute occurrence counts
for attribute in ["ip", "country", "domain", "email"]:
    occurrence_counts = df[attribute].value_counts().head(10)
    
    # Plot the top 10 occurrence counts
    occurrence_counts.plot.bar()
    plt.title(f"Top 10 {attribute} occurrence counts")
    plt.tight_layout()
    # plt.savefig(f"./fig/{attribute}-occurrence-counts.png")
    # plt.show()
    plt.clf()

# # Compute and plot phishing source uptime
# uptimes = pd.DataFrame(np.zeros((len(df), 2)), columns=["ip", "uptime"])

# Convert all dates to datetime objects and add them to the DF
df["start_dt"] = pd.to_datetime(df["firsttime"])
df["end_dt"] = pd.to_datetime(df["lasttime"])

# Unknown lasttimes are indicated as 01-01-1970. We convert these to the date
# on which the data set was last updated.
final_date = max(df.end_dt)
for (index, row) in df.iterrows():
    if row.end_dt.year == 1970:
        df.loc[index, "end_dt"] = final_date

# # Determine whether a given phishing source was active in a given month by giv

# Compute the proportion of unique phishing sources per month
# unique_ips = df.ip.unique()

# Compute the average phishing source uptime per month
month_uptimes = np.zeros(13, dtype=int)
month_row_amnts = np.zeros(13, dtype=int)
for (_, row) in df.iterrows():
    uptime = (row.end_dt - row.start_dt).days

    month = row.start_dt.month
    month_uptimes[month] += uptime
    month_row_amnts[month] += 1

# Normalise each month's uptime
normalised_month_uptimes = month_uptimes.copy()
for month in range(13):
    normalised_month_uptimes[month] /= month_row_amnts[month]

# Plot the average uptime per month
plt.plot()
plt.title(f"Top 10 {attribute} occurrence counts")
plt.tight_layout()
# plt.savefig(f"./fig/{attribute}-occurrence-counts.png")
# plt.show()
plt.clf()

# Compute the percentage of phishing attcks hosted on HTTPS

