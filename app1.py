import pandas as pd
import glob
import os

# Combine files and filter for Pink Morsels
path = 'data'
all_files = glob.glob(os.path.join(path, "daily_sales_data_*.csv"))
df = pd.concat((pd.read_csv(f) for f in all_files), ignore_index=True)

# Data Cleaning
df = df[df['product'] == 'pink morsel']
df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
df['sales'] = df['price'] * df['quantity']
df['date'] = pd.to_datetime(df['date'])

# THIS LINE CREATES THE NEW FILE
df.to_csv("formatted_data.csv", index=False)
print("Success! 'formatted_data.csv' has been created.")
