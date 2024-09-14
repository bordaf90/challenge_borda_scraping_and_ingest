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
WORKDIR /app

# Copy necessary files to the container
COPY scraping.py /app/
COPY requirements.txt /app/

# Install packages from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# The secret file will be mounted at runtime to /run/secrets
# Set the environment variable for the application to use the secret
ENV GOOGLE_APPLICATION_CREDENTIALS="/run/secrets/google_credentials"

# Run the script
CMD ["python", "scraping.py"]
