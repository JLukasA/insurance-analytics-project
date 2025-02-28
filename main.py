import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gamma, kstest
import numpy as np

""" This is the main file run for data analysis, modeling and image generation. I have used it more like a ipynb in this case. """


file_path = "synthetic_insurance_claims.xlsx"

df = pd.read_excel(file_path, sheet_name=1, engine='openpyxl')
df2 = pd.read_excel(file_path, sheet_name=0, engine='openpyxl')

# Print summary table
print(df2)

# Adjust for inflation
inflation = 0.03
df["Adjusted_cost"] = df["Cost"] * ((1 + inflation) ** (2025 - df["Year"]))

# Get inflation adjusted total claims cost and number of liable claims by year
updated_total_cost = df.groupby("Year")["Adjusted_cost"].sum()
updated_total_cost = np.round(updated_total_cost)
liable_claims = df[df["Cost"] > 0].groupby("Year")["Cost"].count()
df3 = pd.DataFrame({"Inflation adjusted total cost ": updated_total_cost, "Liable claims": liable_claims})
print(df3)


# scatterplot by year
plt.figure(figsize=(12, 6))
sns.stripplot(data=df, x="Year", y="Cost", jitter=True, alpha=0.7)
plt.xlabel("Year")
plt.ylabel("Cost of damages")
plt.title("Claims for years 2020-2024")
plt.grid(True)
plt.show()

# extract non-zero values for estimation of distribution
subframe = df[df["Adjusted_cost"] > 0]
print(subframe["Adjusted_cost"].describe())
vals = subframe["Adjusted_cost"].values

# use values to fit a Gamma distribution to the data set.
params = gamma.fit(vals)
shape, loc, scale = params
print(f"shape : {shape}, loc : {loc}, scale : {scale}")


# plot with histogram of non-zero claims values
x = np.linspace(min(vals), max(vals), 100)
pdf = gamma.pdf(x, shape, loc, scale)
plt.figure(figsize=(12, 6))
counts, bin_edges, _ = plt.hist(subframe["Adjusted_cost"], bins=60, density=False, edgecolor="black", alpha=0.7, label="Histogram")
scaling_factor = 100
scaled_counts = counts / scaling_factor
bin_width = bin_edges[1] - bin_edges[0]
plt.figure(figsize=(12, 6))
plt.bar(bin_edges[:-1], scaled_counts, width=bin_width, edgecolor="black", alpha=0.7, label="Scaled Histogram")
plt.plot(x, pdf, 'r-', label="Density function")
plt.xlabel("Claims cost")
plt.ylabel("Density")
plt.title("Gamma density function and histogram of Ajdusted claims costs")
plt.legend()
plt.grid(True)
plt.show()

# kstest
res = kstest(vals, 'gamma', args=params)
print(res)


# Get some probabilities of exceeding certain tresholds of
thresholds = [20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000]
for t in thresholds:
    prob = 1 - gamma.cdf(t, *params)
    print(f"Probability of average cost exceeding {t}: {prob:.2%}")


# Quantiles
threshold_25 = np.round(gamma.ppf(0.75, *params))
threshold_20 = np.round(gamma.ppf(0.80, *params))
threshold_10 = np.round(gamma.ppf(0.90, *params))

print(f"25% probability of average cost exceeding {threshold_25}")
print(f"20% probability of average cost exceeding {threshold_20}")
print(f"10% probability of average cost exceeding {threshold_10}")


premium = 475000
prob_profit_100 = gamma.cdf(((premium - 100000)/(40*0.53)), *params)
prob_profit_100 = 100*np.round(prob_profit_100, 4)
prob_loss_100 = 1 - gamma.cdf(((premium + 100000)/(40*0.53)), *params)
prob_loss_100 = 100*np.round(prob_loss_100, 4)
print(f"{prob_profit_100}% chance of a profit of 100 000 or more with premium at {premium}")
print(f"{prob_loss_100}% chance of a loss of 100 000 or more with premium at {premium}")
