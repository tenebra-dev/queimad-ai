FROM python:3.9-slim-bullseye

WORKDIR /app

    # Install system dependencies for OpenCV
    RUN apt-get update && apt-get install -y \
        libgl1-mesa-glx \
        libglib2.0-0 \
        libsm6 \
        libxext6 \
        libxrender1 \
        libgomp1 \
        libgthread-2.0-0 \
        ffmpeg \
        && rm -rf /var/lib/apt/lists/*

    # Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create directories
RUN mkdir -p models datasets

# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
RUN chown -R appuser:appuser /app
USER appuser

# Expose port for FastAPI (if needed)
EXPOSE 8000

# Command to run the detection script
CMD ["python", "detect.py"]
