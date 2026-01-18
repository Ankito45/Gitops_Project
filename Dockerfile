# Dockerfile for the flask application 
FROM python:3.11-slim

WORKDIR /app

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all of the application code
COPY . .

# Expose port
EXPOSE 5000

# Run the application
CMD ["python", "app/main.py"]