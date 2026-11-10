import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

customers = pd.read_csv('customer_master.csv', header=0)
transactions = pd.read_csv('transactions_log.csv', header=0)

df = pd.merge(transactions, customers,
              how='left',
              on='customer_id',
              indicator=True)

df = df[df['status']=='completed']
df['order_value'] = df['quantity']*df['price']
df['order_date'] = pd.to_datetime(df['order_date'])
df['order_month'] = df['order_date'].dt.to_period('M')


# 1. Line chart — total `order_value` by `order_month`.
monthly = df.groupby('order_month')['order_value'].sum().reset_index()
plt.plot(monthly['order_month'].astype(str), monthly['order_value'], marker='o')
plt.title('Total Revenue by Month')
plt.show()

# 2. Bar chart — total `order_value` by `product`, sorted descending.
product_rev = df.groupby('product')['order_value'].sum().sort_values(ascending=False)
sns.barplot(x=product_rev.index, y=product_rev.values)
plt.xticks(rotation=45)
plt.title("Total Revenue by Month")
plt.show()


# 3. Box plot — `order_value`, confirm the Day 3 outlier visually.
sns.boxplot(x=df['order_value'])
plt.xticks(rotation=45)
plt.show()

# 4. Scatter plot — `quantity` vs `price`, compare to Day 4's weak correlation.
sns.scatterplot(data=df, x="quantity", y="price")
plt.show()


# 5. Interactive version — recreate Task 1 in Plotly, and Task 2 as a Power BI/Tableau dashboard with a month filter.
monthly['order_month'] = monthly['order_month'].astype(str)
fig = px.line(monthly, x="order_month", y="order_value", 
              markers=True,
              title="Interactive Revenue Trend")
fig.show()