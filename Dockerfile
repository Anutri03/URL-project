FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Train the model during build
RUN python save_model.py

# Create a non-root user
RUN useradd -m -u 1000 user && chown -R user:user /app
USER user

# Expose port (Hugging Face uses 7860)
EXPOSE 7860

# Set environment variables
ENV PORT=7860
ENV HOST=0.0.0.0

# Run the application
CMD ["python", "app.py"]
