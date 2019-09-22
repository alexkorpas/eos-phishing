import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import glob

from collections import defaultdict, OrderedDict

# Load the data frame
csv_files = glob.glob("./data/*.csv")
dfs = [pd.read_csv(path, sep='","', engine="python") for path in csv_files]
df = pd.concat(dfs, axis=0)
del dfs  # Garbage collection

# df = pd.read_csv("./data/all_phishing_from_1.csv", sep='","', engine="python")

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

# Compute useful variables for data processing
earliest_year = min(df.start_dt).year
latest_year = max(df.start_dt).year

# # Unknown lasttimes are indicated as 01-01-1970. We convert these to the date
# # on which the data set was last updated.
final_date = max(df.end_dt)
# for (index, row) in df.iterrows():
#     if row.end_dt.year == 1970:
#         df.loc[index, "end_dt"] = final_date

# # Compute the average phishing source uptime per month
# month_uptimes = defaultdict(int)
# month_row_amnts = defaultdict(int)
# for (_, row) in df.iterrows():
#     year = row.start_dt.year
#     month = row.start_dt.month
    
#     # Ignore rows with an unknown start date
#     if year == 1970:
#         continue

#     uptime = (row.end_dt - row.start_dt).days

#     idx = (year - 2000)*12 + month

#     month_uptimes[idx] += uptime
#     month_row_amnts[idx] += 1

# # Normalise each month's uptime
# normalised_month_uptimes = month_uptimes.copy()
# for idx in month_uptimes.keys():
#     if month_row_amnts[idx] == 0:
#         continue
#     normalised_month_uptimes[idx] = month_uptimes[idx]/month_row_amnts[idx]

# # Plot the average uptime per month
# ordered_pairs = OrderedDict(sorted(normalised_month_uptimes.items()))
# keys = [pair[0] for pair in ordered_pairs]
# values = [pair[1] for pair in ordered_pairs]
# plt.bar(keys, values)
# plt.title(f"Average uptime over time")
# plt.ylabel("Days")
# plt.xlabel("Month")
# # plt.tight_layout()
# # plt.savefig(f"./fig/{attribute}-occurrence-counts.png")
# plt.show()

# Compute the percentage of phishing attacks hosted on HTTPS
years = list(range(2006, latest_year + 1))
https_counts = dict.fromkeys(years)
total_counts = dict.fromkeys(years)
for year in years:
    https_counts[year] = 0
    total_counts[year] = 0

for (i, row) in df.iterrows():
    if i % 50000 == 0:
        print(f"Processing index {i}/{len(df)}")

    year = row.start_dt.year
    if year == 1970:
        continue

    if "https" in row.url:
        https_counts[year] += 1
    total_counts[year] += 1

# Compute means
https_proportions = dict.fromkeys(years)
for year in years:
    if total_counts[year] != 0:
        https_proportions[year] = https_counts[year]/total_counts[year]
sorted_https_proportions = sorted(https_proportions.items())
(keys, values) = zip(*sorted_https_proportions)

plt.plot(keys, values)
plt.title("Proportion of phishing sources hosted with HTTPS")
plt.xlabel("Year")
plt.ylabel("Proportion")
# plt.savefig("./fig/https-proportions.png")
plt.show()
