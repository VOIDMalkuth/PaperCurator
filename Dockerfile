# Use python base image
FROM python:3.12-slim

# Set work directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your application files
COPY paper_curator/ ./paper_curator/
COPY scripts/entrypoint.sh .

# Create log directory
RUN mkdir -p /var/log/app
RUN mkdir -p /data

RUN chmod +x ./entrypoint.sh

# Run entrypoint script
ENTRYPOINT ["./entrypoint.sh"]