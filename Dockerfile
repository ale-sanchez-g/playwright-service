FROM mcr.microsoft.com/playwright/python:v1.50.0-jammy

WORKDIR /app

COPY requirements.txt .
# Fix the setuptools vulnerability by upgrading to 70.0+
RUN pip install --upgrade pip setuptools>=70.0
RUN pip install --no-cache-dir -r requirements.txt

# Install additional dependencies and update OpenSSH to address the vulnerability
RUN apt-get update && apt-get install -y \
    curl \
    && apt-get upgrade -y openssh-client openssh-server \
    && rm -rf /var/lib/apt/lists/*

# Copy your application code
COPY . .

RUN playwright install

CMD ["python", "service.py"]