FROM python:3.11-slim

# Step 1: Install system dependencies
RUN echo "🔧 Updating apt and installing Chromium..." && \
    apt-get update && \
    apt-get install -y \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator3-1 \
    libasound2 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    wget \
    curl \
    gnupg && \
    rm -rf /var/lib/apt/lists/* && \
    echo "✅ Chromium and dependencies installed"

# Step 2: Set environment variables for Chrome
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="${CHROME_BIN}:${PATH}"
RUN echo "✅ Environment variables for Chromium set"

# Step 3: Set working directory
WORKDIR /app
RUN echo "✅ Working directory set to /app"

# Step 4: Copy requirements.txt and install Python dependencies
COPY requirements.txt .

RUN apt-get update && \
    apt-get install -y gcc default-libmysqlclient-dev pkg-config && \
    rm -rf /var/lib/apt/lists/* && \
    echo "📦 Installing Python dependencies..." && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    echo "✅ Python dependencies installed"


# Step 5: Copy rest of the project files
COPY . .
RUN echo "📁 Application files copied"

# Final Step: Confirm Docker build complete
RUN echo "✅ Docker build completed successfully"

# Start your app
CMD ["python", "app.py"]
