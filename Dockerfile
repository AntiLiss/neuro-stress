FROM python:3.12.5-slim-bookworm

WORKDIR /app

COPY ./app /app
COPY ./requirements.txt /tmp/requirements.txt

# System deps
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        postgresql-client \
        libpq-dev \
        build-essential && \
    rm -rf /var/lib/apt/lists/*

# Python deps
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt && \
    rm -rf /tmp

RUN mkdir -p /vol/media /vol/static

EXPOSE 8000
