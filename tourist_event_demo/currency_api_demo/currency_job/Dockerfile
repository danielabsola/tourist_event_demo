# Use Python 3.9 slim image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Command to run the application
CMD ["python", "-m", "src.main"]