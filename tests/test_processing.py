import os
import pytest
from backend.app.services.processing import reproject_clip_to_aoi, create_cog, generate_quicklook

def test_reproject_clip(tmp_path):
    src = "tests/data/tiny.tif"
    out = tmp_path / "clipped.tif"
    aoi = {
        "type": "Feature",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[0,0],[0,1],[1,1],[1,0],[0,0]]]
        }
    }
    result = reproject_clip_to_aoi(src, aoi, "EPSG:3857", str(out))
    assert os.path.exists(result)

def test_cog(tmp_path):
    src = "tests/data/tiny.tif"
    out = tmp_path / "cog.tif"
    result = create_cog(src, str(out))
    assert os.path.exists(result)

def test_quicklook(tmp_path):
    src = "tests/data/tiny.tif"
    out = tmp_path / "quicklook.png"
    result = generate_quicklook(src, str(out))
    assert os.path.exists(result)
