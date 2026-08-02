import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from prophet import Prophet
from sklearn.metrics import mean_absolute_error, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

def train_prophet_model(df, test_size=0.2):
    """
    Train Prophet model for sales forecasting
    """
    # Prepare data for Prophet (needs columns 'ds' and 'y')
    prophet_df = df[['Date', 'Weekly_Sales']].copy()
    prophet_df.columns = ['ds', 'y']
    
    # Split data
    train_size = int(len(prophet_df) * (1 - test_size))
    train_df = prophet_df[:train_size]
    test_df = prophet_df[train_size:]
    
    print(f"Training data: {len(train_df)} observations")
    print(f"Test data: {len(test_df)} observations")
    
    # Initialize and train Prophet model
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        changepoint_prior_scale=0.5
    )
    
    model.fit(train_df)
    
    # Make predictions
    future = model.make_future_dataframe(periods=len(test_df), freq='W')
    forecast = model.predict(future)
    
    # Extract predictions for test period
    predictions = forecast.tail(len(test_df))['yhat'].values
    actuals = test_df['y'].values
    
    # Calculate metrics
    mae = mean_absolute_error(actuals, predictions)
    rmse = np.sqrt(mean_squared_error(actuals, predictions))
    mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100
    
    print(f"\nProphet Model Performance:")
    print(f"MAE: ${mae:,.2f}")
    print(f"RMSE: ${rmse:,.2f}")
    print(f"MAPE: {mape:.2f}%")
    
    # Plot results
    fig = model.plot(forecast)
    plt.title('Prophet Forecast')
    plt.xlabel('Date')
    plt.ylabel('Weekly Sales')
    plt.savefig('output/prophet_forecast.png', dpi=300)
    plt.show()
    
    fig2 = model.plot_components(forecast)
    plt.savefig('output/prophet_components.png', dpi=300)
    plt.show()
    
    return model, forecast, {
        'mae': mae,
        'rmse': rmse,
        'mape': mape
    }

if __name__ == "__main__":
    from data_preprocessing import load_and_preprocess_data, resample_data
    
    # Load and prepare data
    df = load_and_preprocess_data('data/train.csv')
    df_weekly = resample_data(df, freq='W')
    
    # Train Prophet model
    model, forecast, metrics = train_prophet_model(df_weekly)
    print("Prophet modeling complete!")