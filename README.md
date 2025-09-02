# GeoETL

End-to-end geospatial ETL platform for satellite imagery.

## Features

- Ingests satellite imagery and metadata from public providers via EODAG (Sentinel-2, Landsat, etc.)
- Tiles, reprojects, clips to AOI, cloud-masks, generates statistics, produces COGs and quicklook PNGs
- Stores raster artifacts in MinIO (S3-compatible), vector/metadata in PostgreSQL + PostGIS
- FastAPI service for task submit/status, catalog browse/search, stats, file/CSV exports
- Prefect 2 for orchestration (flows, schedules)
- CLI for local runs and developer ergonomics
- Unit and integration tests, CI with lint/typecheck/test

## Quickstart

### 1. Clone and start stack

```sh
git clone <repo>
cd geoetl
cp backend/.env.example backend/.env
docker compose up --build -d
make migrate
make seed
```

### 2. Run Prefect UI

```sh
make prefect-ui
# Visit http://localhost:4200
```

### 3. Run a demo ingest job

```sh
curl -X POST "http://localhost:8000/v1/jobs/ingest" \
  -H "X-GEOETL-APIKEY: changeme" \
  -H "Content-Type: application/json" \
  -d '{"aoi": {"type": "Feature", "geometry": {"type": "Polygon", "coordinates": [[[12,48],[12.1,48],[12.1,48.1],[12,48.1],[12,48]]]}}, "start": "2024-01-01", "end": "2024-01-31", "collection": "sentinel-2"}'
```

### 4. Use the CLI

```sh
cd cli
poetry install
poetry run geoetl ingest --aoi ../sample_data/aoi.geojson --start 2024-01-01 --end 2024-01-31 --collection sentinel-2 --use-mock
```

### 5. Run tests and linters

```sh
make test
make lint
make typecheck
```

### 6. Generate presigned URLs

```sh
curl -H "X-GEOETL-APIKEY: changeme" http://localhost:8000/v1/assets/1
```

## API

- `POST /v1/jobs/ingest` — start ingest job
- `GET /v1/jobs/{id}` — job status
- `GET /v1/catalog` — search products
- `GET /v1/assets/{product_id}` — artifact URLs
- `GET /v1/stats/{product_id}` — statistics
- `GET /v1/export/catalog.csv` — CSV export
- `GET /health` — health check

## Configuration

See `.env.example` for all environment variables.

## Architecture

See [docs/architecture.md](docs/architecture.md).

## License

MIT
