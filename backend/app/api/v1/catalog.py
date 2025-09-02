from fastapi import APIRouter, Query, Depends, Response
from sqlalchemy.orm import Session
from typing import Optional, List
from datetime import datetime
from backend.app.db.session import get_db
from backend.app.db.models import Product, Stat
from backend.app.core.config import settings
from backend.app.utils.geo import bbox_to_wkt
import csv
import io

router = APIRouter()

@router.get("/catalog")
def get_catalog(
    bbox: Optional[str] = Query(None, description="minx,miny,maxx,maxy"),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    collection: Optional[str] = Query(None),
    cloud: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if bbox:
        wkt = bbox_to_wkt(bbox)
        query = query.filter(Product.footprint.ST_Intersects(wkt))
    if start:
        query = query.filter(Product.acquisition_time >= start)
    if end:
        query = query.filter(Product.acquisition_time <= end)
    if collection:
        query = query.filter(Product.collection == collection)
    if cloud is not None:
        query = query.filter(Product.cloud_pct <= cloud)
    products = query.all()
    return [p.to_dict() for p in products]

@router.get("/stats/{product_id}")
def get_stats(product_id: int, db: Session = Depends(get_db)):
    stat = db.query(Stat).filter(Stat.product_id == product_id).first()
    if not stat:
        return {"detail": "Not found"}
    return stat.to_dict()

@router.get("/export/catalog.csv")
def export_catalog_csv(
    bbox: Optional[str] = Query(None),
    start: Optional[datetime] = Query(None),
    end: Optional[datetime] = Query(None),
    collection: Optional[str] = Query(None),
    cloud: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    if bbox:
        wkt = bbox_to_wkt(bbox)
        query = query.filter(Product.footprint.ST_Intersects(wkt))
    if start:
        query = query.filter(Product.acquisition_time >= start)
    if end:
        query = query.filter(Product.acquisition_time <= end)
    if collection:
        query = query.filter(Product.collection == collection)
    if cloud is not None:
        query = query.filter(Product.cloud_pct <= cloud)
    products = query.all()
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["id", "provider", "collection", "product_id", "acquisition_time", "cloud_pct"])
    for p in products:
        writer.writerow([p.id, p.provider, p.collection, p.product_id, p.acquisition_time, p.cloud_pct])
    return Response(content=output.getvalue(), media_type="text/csv")
