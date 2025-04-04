FROM python:3.11-slim

# Install Chromium and dependencies
RUN apt-get update && \
    apt-get install -y chromium wget gnupg ca-certificates fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 libatk1.0-0 libcups2 libdbus-1-3 libgdk-pixbuf2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 libxdamage1 libxrandr2 xdg-utils --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set chromium path explicitly in environment
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="$CHROME_BIN:$PATH"

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy your app code
COPY . /app
WORKDIR /app

# Add debug log to confirm Chromium exists
RUN echo "🧪 Checking Chromium binary..." && \
    which chromium && \
    echo "✅ Chromium found!"

# Start your app
CMD ["python", "app.py"]
