import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

def load_and_preprocess_data(file_path):
    """
    Load and preprocess the Walmart sales data
    """
    df = pd.read_csv(file_path, parse_dates=['Date'])
    print(f"Data loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
    
    # Aggregate by date
    df_aggregated = df.groupby('Date')[['Weekly_Sales']].sum().reset_index()
    
    return df_aggregated

def resample_data(df, freq='W'):
    """
    Resample data to weekly frequency
    """
    df_resampled = df.set_index('Date').resample(freq).sum().reset_index()
    print(f"Data resampled to {freq} frequency")
    return df_resampled

def train_arima_model(df, order=(1,1,1), test_size=0.2):
    """
    Train ARIMA model for sales forecasting
    """
    # Prepare data
    df = df.set_index('Date')
    sales_data = df['Weekly_Sales']
    
    # Split data
    train_size = int(len(sales_data) * (1 - test_size))
    train, test = sales_data[:train_size], sales_data[train_size:]
    
    print(f"\nTraining data: {len(train)} observations")
    print(f"Test data: {len(test)} observations")
    
    # Fit ARIMA model
    try:
        model = ARIMA(train, order=order)
        model_fit = model.fit()
        print(model_fit.summary())
        
        # Make predictions
        predictions = model_fit.forecast(len(test))
        
        # Calculate metrics
        mae = mean_absolute_error(test, predictions)
        rmse = np.sqrt(mean_squared_error(test, predictions))
        mape = np.mean(np.abs((test - predictions) / test)) * 100
        
        print(f"\nARIMA Model Performance:")
        print(f"MAE: ${mae:,.2f}")
        print(f"RMSE: ${rmse:,.2f}")
        print(f"MAPE: {mape:.2f}%")
        
        # Visualize results
        fig, axes = plt.subplots(2, 1, figsize=(15, 10))
        
        # Plot predictions vs actual
        axes[0].plot(train.index, train, label='Training Data')
        axes[0].plot(test.index, test, label='Actual Test Data')
        axes[0].plot(test.index, predictions, label='ARIMA Predictions', color='red')
        axes[0].set_title('ARIMA Model: Predictions vs Actual')
        axes[0].set_xlabel('Date')
        axes[0].set_ylabel('Weekly Sales')
        axes[0].legend()
        axes[0].grid(True)
        
        # Plot residuals
        residuals = test - predictions
        axes[1].plot(test.index, residuals)
        axes[1].axhline(y=0, color='r', linestyle='--')
        axes[1].set_title('Prediction Residuals')
        axes[1].set_xlabel('Date')
        axes[1].set_ylabel('Residual')
        axes[1].grid(True)
        
        plt.tight_layout()
        plt.savefig('output/arima_results.png', dpi=300)
        plt.show()
        
        return model_fit, predictions, test, {
            'mae': mae, 
            'rmse': rmse, 
            'mape': mape
        }
        
    except Exception as e:
        print(f"Error training ARIMA model: {e}")
        return None, None, None, None

if __name__ == "__main__":
    # Load and prepare data
    df = load_and_preprocess_data('data/train.csv')
    df_weekly = resample_data(df, freq='W')
    
    # Train ARIMA model
    model, predictions, test, metrics = train_arima_model(df_weekly, order=(1,1,1))
    
    if model:
        print("\nARIMA modeling complete! Check output/arima_results.png for visualization.")