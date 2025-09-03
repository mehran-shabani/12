# Dockerfile
FROM python:3.13-slim

# Create non-root user
RUN groupadd -r django && useradd -r -g django django

WORKDIR /app

# Install system dependencies with pinned versions
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc=4:12.2.0-3 \
    postgresql-client=15+248 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project and set ownership
COPY . .
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Run migrations and collect static files
RUN python manage.py collectstatic --noinput || true

# Add healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/api/patients/ || exit 1

EXPOSE 8000

# For production, use gunicorn:
# CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3"]
# For local dev:
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]