import pandas as pd
from pathlib import Path

# Path to data folder
data_path = Path("data")

# Read all CSV files
files = list(data_path.glob("*.csv"))
df_list = [pd.read_csv(file) for file in files]

# Combine all data
data = pd.concat(df_list, ignore_index=True)

# Keep only Pink Morsels
data = data[data["product"] == "Pink Morsel"]

# Create Sales column
data["Sales"] = data["quantity"] * data["price"]

# Select required fields
final_data = data[["Sales", "date", "region"]]

# Rename columns (optional but clean)
final_data.columns = ["Sales", "Date", "Region"]

# Save output file
final_data.to_csv("formatted_sales_data.csv", index=False)

print("Formatted sales file created successfully.")
