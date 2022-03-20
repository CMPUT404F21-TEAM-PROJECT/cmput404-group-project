# Stage 1 - Install build dependencies
FROM python:3.10-alpine AS builder
WORKDIR /app
COPY requirements.txt .
RUN set -e; \
    apk add --no-cache --virtual .build-deps \
    gcc \
    musl-dev \
    libffi \
    libffi-dev; \
    python -m venv .venv && .venv/bin/pip install --no-cache-dir -U pip setuptools; \
    .venv/bin/pip install --no-cache-dir -r requirements.txt

# Stage 2 - Copy only necessary files to the runner stage
FROM python:3.10-alpine
WORKDIR /app
COPY --from=builder /app /app
COPY . /app
ENV PATH="/app/.venv/bin:$PATH"
CMD sleep 3 && python manage.py makemigrations && python manage.py migrate && python manage.py runserver [::]:8000