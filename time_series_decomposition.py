import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
import warnings
warnings.filterwarnings('ignore')

def perform_decomposition(df, model='additive', period=52):
    """
    Perform time series decomposition
    """
    # Set date as index
    df_decomp = df.set_index('Date')
    
    # Perform decomposition
    decomposition = seasonal_decompose(
        df_decomp['Weekly_Sales'], 
        model=model, 
        period=period
    )
    
    # Create visualization
    fig, axes = plt.subplots(4, 1, figsize=(15, 12))
    
    axes[0].plot(decomposition.observed)
    axes[0].set_title('Original Time Series', fontsize=14)
    axes[0].set_ylabel('Sales')
    
    axes[1].plot(decomposition.trend)
    axes[1].set_title('Trend Component', fontsize=14)
    axes[1].set_ylabel('Sales')
    
    axes[2].plot(decomposition.seasonal)
    axes[2].set_title('Seasonal Component', fontsize=14)
    axes[2].set_ylabel('Sales')
    
    axes[3].plot(decomposition.resid)
    axes[3].set_title('Residual Component', fontsize=14)
    axes[3].set_ylabel('Sales')
    axes[3].set_xlabel('Date')
    
    plt.tight_layout()
    plt.savefig('output/decomposition.png', dpi=300)
    plt.show()
    
    return decomposition

if __name__ == "__main__":
    from data_preprocessing import load_and_preprocess_data, resample_data
    
    # Load and prepare data
    df = load_and_preprocess_data('data/train.csv')
    df_weekly = resample_data(df, freq='W')
    
    # Perform decomposition
    decomposition = perform_decomposition(df_weekly)
    print("Time series decomposition complete!")