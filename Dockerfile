# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.11-slim

# Install system dependencies for Tesseract OCR, OpenCV, and PDF processing.
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container.
WORKDIR /app

# Copy the requirements file first to leverage Docker cache.
COPY requirements.txt .

# Install Python dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code.
COPY . .

# Expose the default Streamlit port.
EXPOSE 8501

# Set Streamlit-specific environment variables for production.
ENV STREAMLIT_SERVER_PORT=8501
ENV STREAMLIT_SERVER_ADDRESS=0.0.0.0
ENV STREAMLIT_SERVER_HEADLESS=true

# Healthcheck to ensure the service is running.
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Command to run the application.
ENTRYPOINT ["streamlit", "run", "app.py"]
