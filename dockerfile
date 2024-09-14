# Use a base Python image
FROM python:3.9-slim

# Install necessary dependencies
RUN apt-get update && \
    apt-get install -y wget unzip \
    libnss3 libgdk-pixbuf2.0-0 libx11-xcb1 libxkbcommon0 libxcomposite1 libxdamage1 libxrandr2 libasound2 libxtst6 libatk-bridge2.0-0 libgtk-3-0 && \
    apt-get install -y curl gnupg && \
    curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable && \
    apt-get clean

# Set the working directory
WORKDIR /proyecto

# Copy the necessary files to the container
COPY scraping.py /proyecto/
COPY challenge-borda-80fb1feb52cb.json /proyecto/
COPY requirements.txt /proyecto/

# Install the packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set the required environment variables
ENV GOOGLE_APPLICATION_CREDENTIALS="/app/challenge-borda-80fb1feb52cb.json"

# Execute the script
CMD ["python", "scraping.py"]
