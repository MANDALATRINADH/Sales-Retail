import pandas as pd
import numpy as np

# Create sample data
dates = pd.date_range(start='2020-01-01', periods=100, freq='D')
sales = np.random.normal(1000, 200, 100) + np.sin(np.arange(100)/10)*300

df = pd.DataFrame({'Date': dates, 'Sales': sales})
df.to_csv('data/sample_data.csv', index=False)

print("Sample data created!")
print(f"Shape: {df.shape}")
print(df.head())
