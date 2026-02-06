# Use official Python 3.11 image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Install requirements if you have a requirements.txt
# Otherwise, install pytest for testing
RUN pip install pytest

# Default command: keep container alive (useful for interactive testing)
CMD ["sleep", "infinity"]
