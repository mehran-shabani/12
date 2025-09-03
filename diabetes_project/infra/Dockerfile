FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create non-root user
RUN useradd -m -u 1000 appuser

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=4:* \
    postgresql-client=15+* \
    libpq-dev=15.* \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip==23.* && pip install --no-cache-dir -r requirements.txt

# Copy project
COPY --chown=appuser:appuser . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Switch to non-root user
USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/health/')" || exit 1

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]