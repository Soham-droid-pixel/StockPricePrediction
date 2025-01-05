# Use the official Python image
FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy the necessary files into the container
COPY . /app

# Install system dependencies required by Matplotlib
RUN apt-get update && apt-get install -y \
    python3-dev \
    libfreetype6-dev \
    libxft-dev \
    libpng-dev \
    libblas-dev \
    liblapack-dev

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port your app will run on
EXPOSE 7860

# Run the app
CMD ["python", "arima_forecast_app.py"]
