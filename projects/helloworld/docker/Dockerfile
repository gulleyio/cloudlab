FROM python:3.14
WORKDIR /app

# Create app user to prevent use of root
RUN useradd appuser
USER appuser

# Install dependencies
COPY ../python/helloworld/requirements.txt ./
RUN pip install -r --no-cache-dir ../python/helloworld/requirements.txt

# Copy source code to workdir
COPY ../python/helloworld .
EXPOSE 8080

ENTRYPOINT [ "uvicorn" ]
CMD ["app.main:app", "--host", "127.0.0.1", "--port", "8080"]
