ARG GDAL_VERSION=3.7.1
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

# Download and install DuckDB extensions for multiple platforms and extension names
# RUN for PLATFORM_NAME in linux_arm64_gcc4 linux_arm64; do \
#     for EXTENSION_NAME in httpfs spatial; do \
#     mkdir -p /root/.duckdb/extensions/v${DUCKDB_VERSION}/${PLATFORM_NAME}; \
#     wget -O /tmp/${EXTENSION_NAME}.duckdb_extension.gz https://extensions.duckdb.org/v${DUCKDB_VERSION}/${PLATFORM_NAME}/${EXTENSION_NAME}.duckdb_extension.gz; \
#     gunzip /tmp/${EXTENSION_NAME}.duckdb_extension.gz; \
#     mv /tmp/${EXTENSION_NAME}.duckdb_extension /root/.duckdb/extensions/v${DUCKDB_VERSION}/${PLATFORM_NAME}/${EXTENSION_NAME}.duckdb_extension; \
#     done; \
#     done

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

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev

ENV PATH="/app/.venv/bin:$PATH"

