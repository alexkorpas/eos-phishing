import pandas as pd
import matplotlib.pyplot as plt
import glob

# Load the data frame
csv_files = glob.glob("./data/*.csv")
dfs = [pd.read_csv(path, sep='","', engine="python") for path in csv_files]
# df = pd.read_csv("./data/all_phishing_from_1.csv", sep='","', engine="python")
df = pd.concat(dfs, axis=0)
del dfs  # Garbage collection

# Compute occurrence counts
for attribute in ["ip", "country", "domain", "email"]:
    occurrence_counts = df[attribute].value_counts().head(10)
    
    # Plot the top 10 occurrence counts
    occurrence_counts.plot.bar()
    plt.title(f"Top 10 {attribute} occurrence counts")
    plt.tight_layout()
    plt.savefig(f"./fig/{attribute}-occurrence-counts.png")
    plt.show()
