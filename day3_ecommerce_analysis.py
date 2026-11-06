 #Task 1: Load and Inspect:** Load the CSV with `pd.read_csv()`. Run `.info()` and `.isnull().sum()` to identify every data quality issue.

import pandas as pd
# import os
# print(os.getcwd())

df = pd.read_csv("ecommerce_orders.csv", header=0)
print(df.head())
print(df.info())
print(df.isnull().sum())

#Task 2 — Clean the Data:
'''
- Standardize the `country` column (trim whitespace, consistent casing).
- Fill missing `quantity` with `1` (a reasonable business assumption for single-item orders).
- Fill missing `price` using the median price for that specific `product` (not the overall median).
- Drop rows with a missing `customer_name` (unidentifiable customers cannot be analyzed per-customer).
'''

df['country'] = df['country'].str.strip().str.lower()
df['quantity'] = df['quantity'].fillna(1)
df['price'] = df.groupby('product')['price'].transform(lambda x: x.fillna(x.median()))
df = df.dropna(subset=['customer_name'])

#Task 3: Flag the Outlier:
# Use the IQR method on a new `order_value` column (`quantity × price`) to detect the outlier order. Do not delete it — add a boolean column `is_outlier` instead, and leave a one-line comment explaining why you chose to flag rather than remove it.

df['order_value'] = df['price']*df['quantity']
Q1 = df['order_value'].quantile(0.25)
Q3 = df['order_value'].quantile(0.75)
IQR = Q3-Q1 
upper_bound = Q3 + 1.5*IQR
lower_bound = Q3 - 1.5*IQR  # < 0

df['is_outlier'] = df['order_value'] > upper_bound
#  Deleting it would understate total revenue and hide a high-value customer from the business. By flagging it instead, you preserve the data for revenue reporting while still giving stakeholders the option to exclude it when they specifically want to see "typical" order behavior (e.g., for average order value calculations).

#Task 4 — Transform: convert `order_date` to datetime, and extract `order_month`.
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_month'] = df['order_date'].dt.month

#Task 5 — Answer These Business Questions:**
'''
1. Who are the top 3 customers by total completed order value?
2. What is the total revenue per month (completed orders only)?
3. After cleaning, does removing the outlier change which customer ranks #1? What does this tell you about relying on a single top-line number?
'''
completed = df[df['status']=='completed'] # only completed orders generated real revenue.
# Q1: Top 3 customers by total order value
top_customers = completed.groupby('customer_name')['order_value'].sum().sort_values(ascending=False).head(3)
print(top_customers)

#Q2: Total revenue per month
monthly_revenue = completed.groupby('order_month')['order_value'].sum()
print(monthly_revenue)

#Q3: 
'''
Removing the outlier will change who rank #1 in Task 5's Q1.
Sum-based rankings can be misleading due to single extreme values. To ensure decisions are based on representative data, we recommend presenting both raw and cleaned datasets, supplemented by secondary performance metrics.
'''



