# Use a lightweight Python image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the project files to the container
COPY . .

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that Gradio uses
EXPOSE 7860

# Command to run the Gradio app
CMD ["python", "arima_forecast_app.py"]
