import typer
import json
from backend.app.flows.ingest import ingest_flow

app = typer.Typer()

@app.command()
def search(aoi: str, start: str, end: str, collection: str, cloud: float = None):
    with open(aoi) as f:
        aoi_geojson = json.load(f)
    result = ingest_flow.search_task(aoi_geojson, start, end, collection, cloud)
    typer.echo(result)

@app.command()
def ingest(aoi: str, start: str, end: str, collection: str, cloud: float = None, use_mock: bool = False):
    with open(aoi) as f:
        aoi_geojson = json.load(f)
    result = ingest_flow(aoi_geojson, start, end, collection, cloud, use_mock)
    typer.echo(result)

@app.command()
def preprocess(src_path: str, aoi: str, dst_crs: str, out_dir: str):
    from backend.app.services.processing import reproject_clip_to_aoi, create_cog, generate_quicklook
    import os, json
    with open(aoi) as f:
        aoi_geojson = json.load(f)
    clipped = reproject_clip_to_aoi(src_path, aoi_geojson, dst_crs, os.path.join(out_dir, "clipped.tif"))
    cog = create_cog(clipped, os.path.join(out_dir, "cog.tif"))
    quicklook = generate_quicklook(cog, os.path.join(out_dir, "quicklook.png"))
    typer.echo({"clipped": clipped, "cog": cog, "quicklook": quicklook})

@app.command()
def publish(local_path: str, bucket: str, object_name: str):
    from backend.app.services.storage import upload_file
    uri = upload_file(local_path, bucket, object_name)
    typer.echo(uri)

if __name__ == "__main__":
    app()
