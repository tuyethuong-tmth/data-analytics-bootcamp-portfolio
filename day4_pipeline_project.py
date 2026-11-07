import pandas as pd
import numpy as np

# Task 1: Merge the data
customers = pd.read_csv('customer_master.csv', header=0)
transactions = pd.read_csv('transactions_log.csv', header=0)

df = pd.merge(transactions, customers,
              how='left',
              on='customer_id',
              indicator=True)
print(df['_merge'].value_counts())
# Why check "_merge" before anything else? This single line immediately reveals data
# integrity issues. Here, it shows one row as "left_only" — the T1007 transaction from
# C08, a customer with no master record. Without `indicator=True`, this transaction would
# silently carry NaN values for customer_name and segment, and you might not notice until
# a later groupby produced a confusing "NaN" category in your report.

# Task 2 — Clean and Transform:** Filter to `status == "completed"`. Create an `order_value` column. Convert `order_date` to datetime and extract `order_month`.
df = df[df['status']=='completed']
df['order_value'] = df['quantity']*df['price']
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_month'] = df['order_date'].dt.to_period('M')

# Task 3 — Pivot Table: Build a pivot table showing total `order_value` with `segment` ("New" vs. "Returning") as rows and `order_month` as columns.
pivot = df.pivot_table(values='order_value',
                       index='segment',
                       columns='order_month',
                       fill_value=0
                       )
print(pivot)

# Task 4 — NumPy Statistics:** Using NumPy, calculate the mean, median, and standard deviation of `order_value`. Then calculate the correlation between `quantity` and `price` across all completed orders.
order_values = df['order_value'].to_numpy()

print('Mean:', np.mean(order_values))
print('Median:', np.median(order_values))
print('Standard deviation (Std Dev):', np.std(order_values))

correlation = np.corrcoef(df['quantity'], df['price'])
print('Correlation:', correlation[0,1])

# Why look at both mean and median together? If they differ substantially (as they do
# here, due to the $8,500 Gaming Chair order), that gap itself is a signal of a skewed
# distribution — the same insight the IQR method captured in Day 3, now confirmed through
# a different statistical lens.


# Task 5 — Synthesize the Findings:
''' Write a short summary (4-6 sentences) answering: 
Which customer segment (New vs. Returning) generates more revenue? 
Is the standard deviation of order value high or low relative to the mean, and what does that suggest about order consistency? 
Is there a meaningful correlation between quantity and price — and does that make business sense?
'''

# Returning customers generated more revenue across three months, largely driven 
# by one high-value order rather than broadly higher spending across the segment.
# The standard deviation of order value is high relative to the mean, which 
# indicates inconsistent order sizes rather than a stable, predictable pattern -
# a single large order can heavily influence monthly totals.
# The correlation between quantity and price is week and slightly negative, which 
# does make some business sense: customers tend to buy more units only of lower-priced
# items, while expensive items are purchased in single units. This week correlation
# confirms that quantity and price are driven by different purchasing behaviors, not 
# by each other.

'''
**Reflection:
The unmatched transaction (`C08`) was deliberately included. 
In a real job, would you silently drop this row, or would you flag it for your manager 
before finalizing the report? Write 2-3 sentences justifying your choice.
'''

# I would not drop the unmatched C08 transaction. Revenue from that order is real and
# should still count toward the company's total monthly revenue - dropping it would
# understate performance. Instead, I would flag it to my manager or the engineering
# team as a data sync issue between the transactions and customer systems, while still
# including its revenue in the top-line numbers (with a clear note that its segment is
# unknown).