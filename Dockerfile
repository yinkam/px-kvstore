FROM python:3.13-slim

WORKDIR /app

COPY key_value_store.py .
COPY server.py .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app

USER app

EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

# Run the server
CMD ["python", "server.py", "--host", "0.0.0.0", "--port", "8000"]