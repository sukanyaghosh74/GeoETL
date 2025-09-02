from sqlalchemy import (
    Column, Integer, String, Float, DateTime, ForeignKey, JSON, Enum, LargeBinary
)
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry
from backend.app.db.base import Base
from datetime import datetime

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(String, nullable=False)
    collection = Column(String, nullable=False)
    product_id = Column(String, unique=True, nullable=False)
    acquisition_time = Column(DateTime, nullable=False)
    cloud_pct = Column(Float)
    properties = Column(JSON)
    footprint = Column(Geometry("POLYGON", srid=4326))
    assets = relationship("Asset", back_populates="product")
    stats = relationship("Stat", back_populates="product")

    def to_dict(self):
        return {
            "id": self.id,
            "provider": self.provider,
            "collection": self.collection,
            "product_id": self.product_id,
            "acquisition_time": self.acquisition_time.isoformat(),
            "cloud_pct": self.cloud_pct,
            "properties": self.properties,
        }

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    kind = Column(String, nullable=False)  # e.g., "COG", "PNG"
    uri = Column(String, nullable=False)
    checksum = Column(String)
    mime = Column(String)
    bytes = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="assets")

class Stat(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    aoi_geom = Column(Geometry("POLYGON", srid=4326))
    ndvi_mean = Column(Float)
    ndvi_std = Column(Float)
    px_count = Column(Integer)
    pct_cloud = Column(Float)
    bands = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    product = relationship("Product", back_populates="stats")

    def to_dict(self):
        return {
            "id": self.id,
            "product_id": self.product_id,
            "ndvi_mean": self.ndvi_mean,
            "ndvi_std": self.ndvi_std,
            "px_count": self.px_count,
            "pct_cloud": self.pct_cloud,
            "bands": self.bands,
            "created_at": self.created_at.isoformat(),
        }

class Job(Base):
    __tablename__ = "jobs"
    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String)
    status = Column(String)
    started_at = Column(DateTime, default=datetime.utcnow)
    finished_at = Column(DateTime, nullable=True)
    log_uri = Column(String, nullable=True)
    params = Column(JSON)

    def to_dict(self):
        return {
            "id": self.id,
            "kind": self.kind,
            "status": self.status,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "log_uri": self.log_uri,
            "params": self.params,
        }
