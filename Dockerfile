# Use a minimal but functional Python image
FROM python:3.11-slim

# Step 1: Install system dependencies (including Chromium & MySQL dev)
RUN echo "🔧 Updating apt and installing dependencies..." && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    chromium \
    chromium-driver \
    pkg-config && \
    rm -rf /var/lib/apt/lists/* && \
    echo "✅ System dependencies installed successfully"

# Step 2: Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH="${CHROME_BIN}:${PATH}"
RUN echo "✅ Environment variables for Chromium set"

# Step 3: Set working directory
WORKDIR /app
RUN echo "✅ Working directory set to /app"

# Step 4: Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN echo "📦 Installing Python dependencies..." && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    echo "✅ Python dependencies installed"

# Step 5: Copy the rest of the application files
COPY . .
RUN echo "📁 Application files copied"

# Step 6: Ensure logs are saved and visible in real-time
RUN mkdir -p logs && touch logs/app.log
ENV LOG_FILE=/app/logs/app.log
RUN echo "✅ Log file set at $LOG_FILE"

# Step 7: Expose necessary port
EXPOSE 10000
RUN echo "✅ Port 10000 exposed"

# Step 8: Final confirmation message before execution
RUN echo "✅ Docker build completed successfully"

# Step 9: Start the application with logs
CMD ["sh", "-c", "echo '🚀 Starting application...' && python app.py 2>&1 | tee -a $LOG_FILE"]
