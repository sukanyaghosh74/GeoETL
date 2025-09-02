from prefect import flow, task, get_run_logger
from backend.app.services.eodag_client import eodag_client
from backend.app.services.processing import reproject_clip_to_aoi, create_cog, generate_quicklook
from backend.app.services.storage import upload_file
from backend.app.services.stats import compute_stats, compute_ndvi
from backend.app.core.config import settings
import os
import uuid

@task
def search_task(aoi, start, end, collection, cloud):
    return eodag_client.search(aoi, start, end, collection, cloud)

@task
def download_task(product_ids, staging_dir, use_mock=False):
    return eodag_client.download(product_ids, staging_dir, use_mock=use_mock)

@task
def preprocess_task(src_path, aoi, dst_crs, out_dir):
    clipped = reproject_clip_to_aoi(src_path, aoi, dst_crs, os.path.join(out_dir, "clipped.tif"))
    cog = create_cog(clipped, os.path.join(out_dir, "cog.tif"))
    quicklook = generate_quicklook(cog, os.path.join(out_dir, "quicklook.png"))
    return {"cog": cog, "quicklook": quicklook}

@task
def publish_task(cog_path, quicklook_path, product_id):
    cog_uri = upload_file(cog_path, settings.MINIO_BUCKET, f"{product_id}/cog.tif")
    quicklook_uri = upload_file(quicklook_path, settings.MINIO_BUCKET, f"{product_id}/quicklook.png")
    return {"cog_uri": cog_uri, "quicklook_uri": quicklook_uri}

@flow
def ingest_flow(aoi, start, end, collection, cloud=None, use_mock=False):
    logger = get_run_logger()
    products = search_task(aoi, start, end, collection, cloud)
    if not products:
        logger.info("No products found")
        return None
    product_ids = [p["id"] for p in products]
    staging_dir = "/tmp/geoetl_staging"
    downloaded = download_task(product_ids, staging_dir, use_mock)
    results = []
    for src_path, prod in zip(downloaded, products):
        out_dir = f"/tmp/geoetl_out/{prod['id']}"
        os.makedirs(out_dir, exist_ok=True)
        processed = preprocess_task(src_path, aoi, settings.DEFAULT_CRS, out_dir)
        published = publish_task(processed["cog"], processed["quicklook"], prod["id"])
        # Compute stats, insert DB rows, etc. (omitted for brevity)
        results.append({
            "product_id": prod["id"],
            "cog_uri": published["cog_uri"],
            "quicklook_uri": published["quicklook_uri"],
        })
    return results

def submit_ingest_job(aoi, start, end, collection, cloud=None):
    # In real deployment, use Prefect API to submit
    flow_run = ingest_flow.submit(aoi, start, end, collection, cloud)
    return str(flow_run.id)

def get_job_status(job_id: str):
    # In real deployment, query Prefect API
    return "running"
