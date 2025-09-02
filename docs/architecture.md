# GeoETL Architecture

## Components

- **FastAPI**: REST API for job submission, catalog, assets, stats, health.
- **Prefect 2**: Orchestration of ETL flows (search, download, preprocess, publish).
- **EODAG**: Provider-agnostic search/download of satellite imagery.
- **Rasterio, rio-cogeo**: Raster processing, COG creation, quicklook PNGs.
- **MinIO**: S3-compatible object storage for raster artifacts.
- **PostGIS**: Vector/metadata storage (footprints, stats, provenance).
- **CLI**: Typer-based, reuses backend code for local runs.
- **Docker Compose**: Local stack for all services.

## Dataflow

1. **User submits job** (API or CLI)
2. **Prefect flow**: search → download → preprocess → publish
3. **Raster artifacts**: COGs, PNGs to MinIO; presigned URLs generated
4. **Metadata**: products, assets, stats, jobs to PostGIS
5. **API**: browse/search, download, stats, CSV export

## CRS Tradeoffs

- Default output: EPSG:3857 (WebMercator) for compatibility
- Native CRS supported (configurable)
- All geometries stored in EPSG:4326 in DB

## COG Rationale

- Tiled, compressed, overviews for efficient cloud access
- Internal overviews: [2,4,8,16]
- BLOCKSIZE=512, DEFLATE, BIGTIFF=IF_SAFER

## Scaling Path

- Dask for distributed raster processing
- Tiling services (e.g., titiler) for web map tiles
- Prefect/Airflow for distributed orchestration

## Limits

- Not for petabyte-scale out-of-the-box
- No user auth/multitenancy (API key only)
- No advanced cloud masking (simple QA band)
