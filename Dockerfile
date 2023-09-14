ARG GDAL_VERSION=3.7.2
FROM ghcr.io/osgeo/gdal:ubuntu-full-${GDAL_VERSION}

LABEL maintainer="Youssef Harby <me@youssefharby.com>"

ARG OS_ARCH=linux \
    PLATFORM_ARCH=aarch64

ENV DUCKDB_VERSION=0.8.1

# Install dependencies
RUN apt-get update && \
    apt-get install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.10 python3-pip python3.10-venv && \
    apt-get install -y unixodbc && \
    python3.10 -m pip install --upgrade pip

# Install duckdb cli
RUN wget https://github.com/duckdb/duckdb/releases/download/v${DUCKDB_VERSION}/duckdb_cli-${OS_ARCH}-${PLATFORM_ARCH}.zip \
    && unzip duckdb_cli-${OS_ARCH}-${PLATFORM_ARCH}.zip -d /usr/local/bin \
    && rm duckdb_cli-${OS_ARCH}-${PLATFORM_ARCH}.zip

# Update shared library cache
RUN ldconfig

# Install Poetry
RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock config.yml ./
COPY README.md ./
COPY overturemapsdownloader ./overturemapsdownloader

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --extras "gdal_support"

ENV PATH="/app/.venv/bin:$PATH"

