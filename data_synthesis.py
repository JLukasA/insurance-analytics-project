import numpy as np
import pandas as pd
from scipy.stats import gamma
from datetime import datetime, timedelta


""" This is a short script to synthesise data for a insurance claim analytics case. The data is written to a two-sheet xlsx-file, where the
    first sheet contains a small summary table and the second sheet contains individual insurance claims.

    Some information about the data:
    - contains data for years 2020-2024
    - strictly increasing number of cars covered by insurance, starting at 85 year 2020 and allowing a max of 115 cars to be covered by insurance in 2024
    - a 3% yearly inflation is assumed
    - Although one would expect a seasonal trend in this type of data, I have not included is since the case is about yearly insurance coverage.
    - Each year has a separate (and adjustable):
        - Number of claims per insured car
        - Liability ratio
        - Distribution of Liable claims costs
 """

np.random.seed(1)
years = np.arange(2020, 2025)

# cars per year, start at 85, max 115 by 2024
insured_cars = []
min_cars = 85
max_cars = 115
for _ in years:
    num_cars = min(np.random.randint(min_cars, max_cars + 1), 115)
    insured_cars.append(num_cars)
    min_cars = num_cars

# Generate insurance claims by year.
# First generate number of claims
# Then apply liability ratio to get number of liable claims and zero-valued claims
# Finally, generate a gamma distribution to use for liable claims costs
claims_data = []
summary_data = {"Year": [], "Cost": [], "Accidents": [], "Cars": []}
for year, num_cars in zip(years, insured_cars):
    num_claims = int(np.random.uniform(0.32, 0.38) * num_cars)  # Number of claims

    # Zero-valued claims (AKA non-liable)
    zero_claims_ratio = np.random.uniform(0.45, 0.52)
    num_zero_claims = int(num_claims * zero_claims_ratio)

    # liable claims
    shape = np.random.uniform(0.8, 1.0)  # Slightly vary shape
    scale = np.random.uniform(13500, 14500)  # Slightly vary scale
    inflation = 0.03
    scale = scale * ((1 + inflation) ** (year - 2020))
    non_zero_claims = gamma.rvs(shape, loc=315, scale=scale, size=(num_claims - num_zero_claims))
    non_zero_claims = np.round(non_zero_claims)

    # add non-laible and liable together and shuffle values
    claim_values = np.concatenate((np.zeros(num_zero_claims), non_zero_claims))
    np.random.shuffle(claim_values)

    # Generate random accident dates within the year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    accident_dates = [start_date + timedelta(days=np.random.randint(0, 365)) for _ in range(num_claims)]

    # Fill summary table row
    total_cost = np.sum(non_zero_claims)
    summary_data["Year"].append(year)
    summary_data["Cost"].append(total_cost)
    summary_data["Accidents"].append(num_claims)
    summary_data["Cars"].append(num_cars)

    # create claims by combining shuffled values with generated random dates
    for date, claim_value in zip(accident_dates, claim_values):
        claims_data.append([date.strftime("%Y-%m-%d"), year, claim_value])

# Save to xlsx
summary_df = pd.DataFrame(summary_data)
columns = ["Date", "Year", "Cost"]
claims_df = pd.DataFrame(claims_data, columns=columns)
with pd.ExcelWriter("synthetic_insurance_claims.xlsx") as writer:
    summary_df.to_excel(writer, sheet_name="Summary", index=False)
    claims_df.to_excel(writer, sheet_name="Claims", index=False)

print("Synthetic insurance claims data generated and saved to 'synthetic_insurance_claims.xlsx'")
