import pandas as pd
import sqlite3

'''
CLEANED AND IMPORT CSV FILES INTO SQLITE DATABASE
====================================================
code
```
# As we can not import reviews file into SQLite, we will clean the data first
df = pd.read_csv('/Users/tuyethuong/Downloads/olist/olist_order_reviews_dataset.csv')

# Trim leading/trailing spaces and tabs in columns names and text cells
df.columns = df.columns.str.strip()
df = df.apply(lambda col: col.str.strip() if col.dtype == "string" else col)

# Remove tabs and line breaks inside cells while preserving ordinary spaces:
df = df.replace(r"[\t\r\n]+", " ", regex=True)
df = df.apply(lambda col: col.str.strip() if col.dtype == "string" else col)

# Export new reviews csv file
df.to_csv('/Users/tuyethuong/Downloads/olist/cleaned_reviews.csv', index=False, encoding='utf-8')

# Import into SQLite
# Find your db path on Dbeaver using: PRAGMA database_list;

with sqlite3.connect("/Applications/DBeaverUltimate.app/Contents/MacOS/practice.db") as conn:
    df.to_sql("reviews", conn, if_exists="replace", index=False)
```
'''
conn = sqlite3.connect("/Applications/DBeaverUltimate.app/Contents/MacOS/practice.db")
orders = pd.read_sql_query("SELECT * FROM orders", conn)
payments = pd.read_sql_query("SELECT * FROM payments", conn)
reviews = pd.read_sql_query("SELECT * FROM reviews", conn)

# `orders` - one row per order, including purchase and delivery timestamp.
# `payments` - an order can have more than one payment.
# `reviews` -  one review should connect with an order, an order can have more than one review.

# Central Tendency
payment_value = payments["payment_value"]

mean_value = payment_value.mean()
median_value = payment_value.median()
mode_value = payment_value.mode()[0]

print(f'Mean: {mean_value:.2f} | Median: {median_value:.2f} | Mode: {mode_value:.2f}')
# Mean > Median > Mode indicates that the data has right-skewed distribution.
# The discrepancy between the Mean and the Median suggests the presence of outliers.

# Dispersion
value_range = payment_value.max() - payment_value.min()
variance = payment_value.var()
std_dev = payment_value.std()

print(f"Range: {value_range:.2f} | Variance: {variance:.2f} | Std Dev: {std_dev:.2f}")
# An extremely large range, combined with a standard deviation that exceeds the mean, 
# indicates a very high degree of data dispersion; in such cases, neither the mean nor 
# the standard deviation accurately represents the dataset. 

# The Normal Distribution
import matplotlib.pyplot as plt
import seaborn as sns

sns.histplot(payment_value, kde=True, bins=40)
plt.title('Distribution of Payment Values')
plt.xlabel('Payment Value (R$)')
plt.show()