from shapely.geometry import shape, box, mapping
from shapely.ops import transform
import pyproj
import json

def validate_aoi(aoi_geojson: dict) -> bool:
    try:
        geom = shape(aoi_geojson["geometry"])
        return geom.is_valid and geom.geom_type == "Polygon"
    except Exception:
        return False

def bbox_to_wkt(bbox: str) -> str:
    minx, miny, maxx, maxy = map(float, bbox.split(","))
    geom = box(minx, miny, maxx, maxy)
    return geom.wkt

def reproject_geom(geom: dict, from_crs: str, to_crs: str) -> dict:
    project = pyproj.Transformer.from_crs(from_crs, to_crs, always_xy=True).transform
    s = shape(geom)
    s2 = transform(project, s)
    return mapping(s2)
