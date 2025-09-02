from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.app.db.session import get_db
from backend.app.db.models import Asset
from backend.app.services.storage import get_presigned_url

router = APIRouter()

@router.get("/assets/{product_id}")
def get_assets(product_id: int, db: Session = Depends(get_db)):
    assets = db.query(Asset).filter(Asset.product_id == product_id).all()
    result = []
    for asset in assets:
        url = get_presigned_url(asset.uri)
        result.append({
            "id": asset.id,
            "kind": asset.kind,
            "uri": asset.uri,
            "url": url,
            "mime": asset.mime,
            "bytes": asset.bytes,
            "created_at": asset.created_at,
        })
    return result
