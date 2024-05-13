# Use the official lightweight Python image
FROM python:3.9-slim

# Set environment variables to avoid Python buffering issues
ENV PYTHONUNBUFFERED=1
ENV PORT=8080
ENV RUNNING_IN_DOCKER=true

# Set working directory
WORKDIR /app

# Copy the requirements.txt file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install necessary dependencies for Selenium and geckodriver
RUN apt-get update && apt-get install -y \
    wget \
    firefox-esr \
    xvfb \
    libdbus-glib-1-2 \
    libxt6 \
    ca-certificates \
    fonts-liberation \
    libasound2 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdbus-1-3 \
    libgdk-pixbuf2.0-0 \
    libnspr4 \
    libnss3 \
    libx11-6 \
    libxcomposite1 \
    libxcursor1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxi6 \
    libxrandr2 \
    libxrender1 \
    libxss1 \
    libxtst6 \
    xdg-utils

# Install geckodriver
RUN wget -q "https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz" -O geckodriver.tar.gz \
    && tar -xzf geckodriver.tar.gz -C /usr/bin \
    && chmod +x /usr/bin/geckodriver \
    && rm geckodriver.tar.gz

# Copy all the application files
COPY . .

# Expose the port Streamlit runs on
EXPOSE 8080

# Run Streamlit on the dynamically assigned PORT
CMD ["streamlit", "run", "main.py", "--server.port", "8080", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"]
# CMD ["streamlit", "run", "main.py"]
# 