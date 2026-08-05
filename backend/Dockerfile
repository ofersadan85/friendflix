# FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
FROM ghcr.io/astral-sh/uv:python3.13-alpine

WORKDIR /app
COPY pyproject.toml uv.lock .python-version /app/
RUN --mount=type=cache,target=/root/.cache/uv uv sync --no-dev --locked

COPY . .
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000
CMD ["fastapi", "run", "--host", "0.0.0.0", "--port", "8000"]
