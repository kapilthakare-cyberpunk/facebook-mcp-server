FROM python:3.13-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir uv

# Copy dependency manifests and README first for caching
COPY pyproject.toml uv.lock README.md ./

# Copy the full source BEFORE running uv sync so Hatchling sees your package files
COPY src ./src

# Now install dependencies including the project itself, no editable install if using --no-editable
RUN uv sync --frozen --no-dev --no-editable

# Default command
CMD ["uv", "run", "facebook-mcp-server"]

