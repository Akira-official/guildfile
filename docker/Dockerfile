FROM python:3.11-slim

# Prevent python from buffering stdout/stderr
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code and templates
COPY src/ ./src/
COPY templates/ ./templates/
COPY pyproject.toml .

# Install package in editable mode
RUN pip install --no-cache-dir -e .

CMD ["python", "-m", "src.cli.main", "agent"]
