# Overture Maps Downloader

This repository is still under heavy development. Features may change, and documentation will be updated accordingly. Use at your own risk and feel free to contribute!

## Overview

OvertureMapsDownloader is a comprehensive tool designed to streamline the process of querying, downloading, and converting Overture Maps data. Leveraging modern technologies like DuckDB, Dask DataFrames, and GDAL/OGR, this tool offers a containerized solution that seamlessly integrates with your existing pipelines and ETL workflows. Whether you're a data scientist, a geospatial analyst, or a developer.

For hands-on examples, check out the Jupyter notebooks available in the `examples` folder.

## Table of Contents

- [OvertureMapsDownloader]
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Usage](#usage)
    - [Download Geospatial Data](#download-geospatial-data)
    - [Convert to GeoPackage](#convert-to-geopackage)
- [Initialize Typer app](#initialize-typer-app)
  - [Using Jupyter Notebooks](#using-jupyter-notebooks)
  - [Configuration](#configuration)

## Prerequisites

- Docker and Docker Compose
- GeoJSON file containing the bounding box polygon (e.g., `bbox.geojson`)
  **you can make yours easly on https://geojson.io or use `examples/bbox.json` for testing**

## Installation

To get started, you'll need to pull the Docker image from the GitHub Container Registry:

```bash
docker pull ghcr.io/youssef-harby/overturemapsdownloader:latest
```

## Usage

### Download Geospatial Data

1. Create a folder and place your bounding box polygon in GeoJSON format inside it (e.g., `bbox.geojson`).
2. Navigate to the folder:

   ```bash
   cd /path/to/your/folder # e.g., cd /examples
   ```

3. Run the following command to download geospatial data:

   ```bash
   docker run -v $(pwd):/examples --name omdownloader ghcr.io/youssef-harby/overturemapsdownloader:latest OMDownloader omaps --theme places --ptype place --bbox /examples/bbox.geojson --output /examples/places.parquet
   ```

#### Commands

The omaps Command

```bash
OMDownloader omaps [OPTIONS]
```

options:

- `--theme [admins|buildings|buildings|places|transportation]` Theme of the data to download
- `--ptype [locality|administrativeBoundary|building|place|water|connector|segment]` Type of the data to download
- `--bbox PATH` Bounding box polygon in GeoJSON format as a path to a file
- `--output PATH` Output file path (e.g., `places.parquet`)
- `--help` Show this message and exit.

### Convert Parquet to GeoPackage

To convert the downloaded data to GeoPackage format, run the following command:

```bash
docker run -v $(pwd):/examples --name omdownloader ghcr.io/youssef-harby/overturemapsdownloader:latest ogr2ogr /examples/output.gpkg /examples/places.parquet
```

### Convert Parquet to MBTiles (will support tippecanoe in the future)

```bash
docker run -v $(pwd):/examples ghcr.io/youssef-harby/overturemapsdownloader:latest ogr2ogr -dsco MAXZOOM=14 /examples/output.mbtiles /examples/places.parquet
```

### Convert Parquet to ESRI File Geodatabase vector (OpenFileGDB)

```bash
docker run -v $(pwd):/examples ghcr.io/youssef-harby/overturemapsdownloader:latest ogr2ogr /examples/output.gdb /examples/places.parquet
```

## Using Jupyter Notebooks (Data Scientists/GIS Analysts)

If you prefer to use Jupyter notebooks for your geospatial data manipulation tasks, you can easily set up a Jupyter environment using Docker Compose.

1. Clone the repository:

   ```bash
   git clone https://github.com/Youssef-Harby/OvertureMapsDownloader.git
   ```

2. Navigate to the repository folder:

   ```bash
   cd OvertureMapsDownloader
   ```

3. Run the following Docker Compose command:

   ```bash
   docker compose up
   ```

This will start a Jupyter notebook server accessible at http://localhost:8888/lab.

## Configuration

For advanced configurations, please refer to the `config.yml` file.
