# Inspired from: https://github.com/astral-sh/uv-docker-example/blob/main/multistage.Dockerfile
# ─────────────────────────────────────────────
# 🚧 Stage 1: Build application and dependencies
# Uses Astral's UV Python manager on slim Debian (Bookworm)
# ─────────────────────────────────────────────
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder

# Optimize UV and Python settings for reproducible builds
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_INSTALL_DIR=/python \
    UV_PYTHON_PREFERENCE=only-managed

# Install Python 3.13.3 into /python (only managed versions)
RUN uv python install 3.13.3

# Define working directory
WORKDIR /app

# Install base dependencies (but not project code or dev packages)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev

# Copy project source after installing dependencies
COPY pyproject.toml uv.lock Makefile .env.prod manage.py ./
COPY src ./src
COPY public ./public

# Install project itself (as a library, but no dev tools)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# ─────────────────────────────────────────────
# 🐳 Stage 2: Final minimal runtime image
# Based on Debian slim, only includes Python and runtime code
# ─────────────────────────────────────────────
FROM debian:bookworm-slim

# Install only essential tools (make, curl, ca-certificates), then clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    make curl ca-certificates && \
    apt-get purge -y --auto-remove && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy managed Python runtime and installed virtualenv
COPY --from=builder --chown=python:python /python /python
COPY --from=builder --chown=app:app /app /app

# Set environment
ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONPATH="/app/src"

# Add entrypoint script
COPY docker/entrypoints/prod/api.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Default entrypoint
ENTRYPOINT ["/entrypoint.sh"]
