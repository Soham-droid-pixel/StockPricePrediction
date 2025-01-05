import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from prophet import Prophet
import gradio as gr
import gradio as gr
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt

# ARIMA Forecast Function
def arima_forecast(data, steps=30):
    """
    ARIMA-based forecasting function.
    """
    # Fit ARIMA model
    model = ARIMA(data, order=(5, 1, 0))
    model_fit = model.fit()

    # Generate forecast
    forecast = model_fit.forecast(steps=steps)

    # Prepare the forecast data as a DataFrame with 'Date' column
    future_dates = pd.date_range(start=data.index[-1], periods=steps + 1, freq="D")[1:]
    forecast_df = pd.DataFrame({"Date": future_dates, "Predicted Price": forecast})
    return forecast_df

# Plotting Function
def plot_forecast(df, forecast_df, model_name="ARIMA"):
    """
    Plots the forecast results.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['Adjusted Close'], label='Historical Data')
    plt.plot(forecast_df['Date'], forecast_df['Predicted Price'], label=f'{model_name} Forecast', linestyle='--')
    plt.title(f'{model_name} Stock Price Forecast')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.legend()

    plot_path = "forecast_plot.png"
    plt.savefig(plot_path)
    plt.close()

    return plot_path

# Main Forecasting Function
def forecast_stock(file, manual_data, steps):
    """
    Main function to handle ARIMA forecasting and return results.
    """
    if file is not None:
        # Use uploaded file
        df = pd.read_csv(file)
    elif manual_data is not None:
        # Use manually entered data
        df = pd.DataFrame(manual_data)

    # Ensure Date column is parsed
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df = df[['Adjusted Close']]

    # Generate forecast
    forecast_df = arima_forecast(df, steps)
    
    # Plot forecast
    plot_path = plot_forecast(df, forecast_df, model_name="ARIMA")

    # Return plot and forecast table
    return plot_path, forecast_df

# Gradio Interface
def stock_ui():
    with gr.Blocks() as app:
        gr.Markdown("## ARIMA Stock Price Forecasting")
        gr.Markdown("Upload a file or manually input stock data (parsed 'Date' column required).")

        # File Upload
        file_input = gr.File(label="Upload Stock Data (CSV)")

        # Manual Data Entry
        manual_data_input = gr.DataFrame(headers=["Date", "Adjusted Close"], label="Manual Data Entry")

        # Steps for Forecasting
        steps_input = gr.Number(label="Forecast Steps (Days)", value=30)

        # Outputs
        output_plot = gr.Image(label="Forecast Plot")
        output_table = gr.DataFrame(label="Predicted Prices")

        # Button
        btn = gr.Button("Generate Forecast")
        btn.click(
            forecast_stock,
            inputs=[file_input, manual_data_input, steps_input],
            outputs=[output_plot, output_table]
        )

    return app

# Launch Gradio app
app = stock_ui()
app.launch('share=True')
