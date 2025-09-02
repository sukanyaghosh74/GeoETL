# GeoETL

GeoETL is an end‑to‑end geospatial ETL (Extract‑Transform‑Load) platform tailored for satellite imagery processing, data management, and developer ergonomics.

---

## Features

* **Satellite imagery ingestion**: Pulls data and metadata from public providers such as Sentinel‑2 and Landsat via EODAG.
* **Processing pipeline**: Tiles, reprojects, clips to AOI (Area of Interest), applies cloud masks, generates statistics, and produces Cloud-Optimized GeoTIFFs (COGs) and quicklook PNG images.
* **Artifact storage**:

  * Raster outputs: Stored in MinIO (S3‑compatible bucket).
  * Vectors and metadata: Persisted in PostgreSQL with PostGIS.
* **API service**: Built using FastAPI to manage workflows:

  * Task submission and status tracking
  * Catalog browsing and search
  * Statistics retrieval
  * File and CSV exports
* **Orchestration**: Managed by Prefect 2, enabling flow scheduling and workflow management.
* **Command-line interface (CLI)**: Simplifies local runs for developers.
* **Testing and CI coverage**: Includes unit and integration tests with linting and type checking.

---

## Quickstart Guide

### 1. Clone and initialize the stack

```bash
git clone https://github.com/sukanyaghosh74/GeoETL.git
cd GeoETL
cp backend/.env.example backend/.env
docker-compose up --build -d
make migrate
make seed
```

### 2. Launch Prefect UI

```bash
make prefect-ui
# Visit http://localhost:4200 in your browser
```

### 3. Start a demo ingestion job

```bash
curl -X POST "http://localhost:8000/v1/jobs/ingest" \
  -H "X-GEOETL-APIKEY: changeme" \
  -H "Content-Type: application/json" \
  -d '{
    "aoi": {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [[[12,48],[12.1,48],[12.1,48.1],[12,48.1],[12,48]]]
      }
    },
    "start": "2024-01-01",
    "end": "2024-01-31",
    "collection": "sentinel-2"
}'
```

### 4. Use the CLI tool

```bash
cd cli
poetry install
poetry run geoetl ingest \
  --aoi ../sample_data/aoi.geojson \
  --start 2024-01-01 \
  --end 2024-01-31 \
  --collection sentinel-2 \
  --use-mock
```

### 5. Run tests and linters

```bash
make test
make lint
make typecheck
```

### 6. Retrieve presigned URLs for artifacts

```bash
curl -H "X-GEOETL-APIKEY: changeme" http://localhost:8000/v1/assets/1
```

---

## API Reference

* `POST /v1/jobs/ingest` – Start an ingestion job
* `GET /v1/jobs/{id}` – Check job status
* `GET /v1/catalog` – Search product catalog
* `GET /v1/assets/{product_id}` – Retrieve asset download links and metadata

---

## Why GeoETL?

GeoETL bridges the gap between raw satellite imagery and actionable geospatial insights. With automated ingestion, standardized pipelines, and scalable storage, it simplifies geospatial ETL workflows while remaining developer‑friendly.

---

## Contributing

Contributions are welcome. Fork the repo, create a branch, and submit a pull request with your improvements. Bug reports and feature requests can be filed through GitHub Issues.

---

## License

GeoETL is distributed under the MIT License. See the `LICENSE` file for full details.
