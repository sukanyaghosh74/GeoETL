import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    DB_URL: str = os.getenv("DB_URL", "postgresql+psycopg2://geoetl:geoetl@db:5432/geoetl")
    MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "minio:9000")
    MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
    MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
    MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "geoetl-artifacts")
    EODAG_CONFIG_PATH: str = os.getenv("EODAG_CONFIG_PATH", "/app/eodag.yml")
    API_KEY: str = os.getenv("GEOETL_API_KEY", "changeme")
    PREFECT_API_URL: str = os.getenv("PREFECT_API_URL", "http://prefect:4200/api")
    COG_COMPRESSION: str = os.getenv("COG_COMPRESSION", "DEFLATE")
    COG_BLOCKSIZE: int = int(os.getenv("COG_BLOCKSIZE", "512"))
    COG_OVERVIEWS: str = os.getenv("COG_OVERVIEWS", "2,4,8,16")
    DEFAULT_CRS: str = os.getenv("DEFAULT_CRS", "EPSG:3857")
    DEFAULT_COLLECTION: str = os.getenv("DEFAULT_COLLECTION", "sentinel-2")
    DEFAULT_AOI_PATH: str = os.getenv("DEFAULT_AOI_PATH", "/app/sample_data/aoi.geojson")
    class Config:
        env_file = ".env"

settings = Settings()
