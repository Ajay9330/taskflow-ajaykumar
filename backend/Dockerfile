# -----------------------------
# Stage 1 — builder
# -----------------------------
FROM python:3.13-slim AS builder

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency definition
COPY pyproject.toml ./

# Install dependencies from pyproject.toml
RUN uv pip install --system .

# Copy application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .


# -----------------------------
# Stage 2 — runtime
# -----------------------------
FROM python:3.13-slim

WORKDIR /app

# Create non-root user
RUN groupadd -r appgroup && useradd -r -m -g appgroup appuser

# Copy installed dependencies
COPY --from=builder /usr/local /usr/local

# Copy application code
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .
COPY scripts ./scripts

# Fix permissions
RUN chown -R appuser:appgroup /app && chmod +x scripts/start.sh

USER appuser

EXPOSE 8080

CMD ["scripts/start.sh"]