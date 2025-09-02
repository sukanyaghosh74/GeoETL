from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional
from backend.app.flows.ingest import submit_ingest_job, get_job_status
from backend.app.db.session import get_db
from backend.app.db.models import Job
from sqlalchemy.orm import Session

router = APIRouter()

class IngestJobRequest(BaseModel):
    aoi: dict
    start: str
    end: str
    collection: str
    cloud: Optional[float] = None

@router.post("/jobs/ingest")
def ingest_job(
    req: IngestJobRequest,
    db: Session = Depends(get_db)
):
    job_id = submit_ingest_job(req.aoi, req.start, req.end, req.collection, req.cloud)
    # Optionally, insert job row here
    job = Job(
        kind="ingest",
        status="submitted",
        params=req.dict(),
    )
    db.add(job)
    db.commit()
    db.refresh(job)
    return {"job_id": job_id, "db_id": job.id}

@router.get("/jobs/{job_id}")
def get_job(job_id: str, db: Session = Depends(get_db)):
    status = get_job_status(job_id)
    job = db.query(Job).filter(Job.id == job_id).first()
    return {
        "job_id": job_id,
        "status": status,
        "db_row": job.to_dict() if job else None
    }
