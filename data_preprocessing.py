import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data(file_path):
    df = pd.read_csv(file_path, parse_dates=['Date'])
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    df_aggregated = df.groupby('Date')[['Weekly_Sales']].sum().reset_index()
    df_aggregated['Year'] = df_aggregated['Date'].dt.year
    df_aggregated['Month'] = df_aggregated['Date'].dt.month
    df_aggregated['Day'] = df_aggregated['Date'].dt.day
    df_aggregated['DayOfWeek'] = df_aggregated['Date'].dt.dayofweek
    return df_aggregated

def resample_data(df, freq='W'):
    df_resampled = df.set_index('Date').resample(freq).sum().reset_index()
    print(f"Data resampled to {freq} frequency")
    return df_resampled

def visualize_data(df):
    fig, axes = plt.subplots(3, 1, figsize=(15, 12))
    axes[0].plot(df['Date'], df['Weekly_Sales'])
    axes[0].set_title('Weekly Sales Over Time', fontsize=14)
    axes[0].set_xlabel('Date')
    axes[0].set_ylabel('Weekly Sales')
    axes[0].grid(True)
    df_copy = df.copy()
    df_copy['Month'] = df_copy['Date'].dt.month
    df_copy.boxplot(column='Weekly_Sales', by='Month', ax=axes[1])
    axes[1].set_title('Monthly Sales Distribution', fontsize=14)
    axes[1].set_xlabel('Month')
    axes[1].set_ylabel('Sales')
    df_copy['Year'] = df_copy['Date'].dt.year
    for year in df_copy['Year'].unique():
        yearly_data = df_copy[df_copy['Year'] == year]
        axes[2].plot(yearly_data['Date'], yearly_data['Weekly_Sales'], label=f'Year {year}', alpha=0.7)
    axes[2].set_title('Yearly Sales Comparison', fontsize=14)
    axes[2].set_xlabel('Date')
    axes[2].set_ylabel('Sales')
    axes[2].legend()
    axes[2].grid(True)
    plt.tight_layout()
    plt.savefig('output/sales_visualization.png', dpi=300)
    plt.show()
    return fig

if __name__ == "__main__":
    df = load_and_preprocess_data('data/train.csv')
    df_weekly = resample_data(df, freq='W')
    visualize_data(df_weekly)
    print("✅ Data preprocessing complete!")
