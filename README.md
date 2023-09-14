```bash
docker run -v $(pwd):examples ghcr.io/youssef-harby/overturemapsdownloader:latest OMDownloader omaps --theme places --ptype place --bbox examples/bbox.geojson --output examples/places.parquet
```
