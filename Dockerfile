# Base image with Python and Chrome
FROM python:3.11-slim

# Install Chromium and dependencies
RUN apt-get update && apt-get install -y \
    chromium chromium-driver \
    fonts-liberation libappindicator3-1 xdg-utils wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set display and Chrome path
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="$PATH:/usr/bin"

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run your app (modify if needed)
CMD ["python", "app.py"]
