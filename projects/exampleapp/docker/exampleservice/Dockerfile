FROM python:3.14-alpine as builder

# Set directory
WORKDIR /app

# Install prerequisites
RUN apk add binutils

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:0.9.26  /uv /uvx /bin/

# Copy the application into the container.
COPY . .

# Install dependencies
RUN uv sync --frozen --no-cache

# Build
RUN uv run pyinstaller --noconfirm --onefile --name /app/example-api /app/main.py

FROM alpine:latest

# Create user
RUN addgroup -S appgroup && adduser -S serviceuser -G appgroup

WORKDIR /app

COPY --from=builder /app/dist/example-api /app/example-api

RUN chown -R serviceuser:appgroup /app

USER serviceuser
EXPOSE 8088
CMD [ "/app/example-api" ]
# Run the application.
# ENTRYPOINT [ "/app/.venv/bin/fastapi", "run", "app/main.py" ]
# CMD [ "--port", "8088", "--host", "0.0.0.0"]
