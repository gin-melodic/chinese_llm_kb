FROM python:3.10-slim

WORKDIR /app

# Copy dependency files
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt
# If you are in China, you can use the following command to install dependencies
# RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app

# Expose ports
EXPOSE 8000

# Start command
CMD ["python", "run.py"]
