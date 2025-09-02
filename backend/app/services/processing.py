import rasterio
from rasterio.enums import Resampling
from rasterio.io import MemoryFile
from rasterio.warp import calculate_default_transform, reproject
from rasterio.mask import mask
from rio_cogeo.cogeo import cog_translate, cog_validate
from rio_cogeo.profiles import cog_profiles
import numpy as np
from shapely.geometry import shape, mapping
import os
from typing import Tuple, Dict, Any, Optional
from PIL import Image

def reproject_clip_to_aoi(src_path: str, aoi_geojson: dict, dst_crs: str, out_path: str) -> str:
    with rasterio.open(src_path) as src:
        geom = [shape(aoi_geojson["geometry"])]
        out_image, out_transform = mask(src, [mapping(g) for g in geom], crop=True)
        out_meta = src.meta.copy()
        out_meta.update({
            "driver": "GTiff",
            "height": out_image.shape[1],
            "width": out_image.shape[2],
            "transform": out_transform,
            "crs": dst_crs,
        })
        with rasterio.open(out_path, "w", **out_meta) as dest:
            dest.write(out_image)
    return out_path

def create_cog(src_path: str, dst_path: str, blocksize: int = 512, compression: str = "DEFLATE", overviews=(2,4,8,16)) -> str:
    profile = cog_profiles.get("deflate")
    profile.update(
        BLOCKSIZE=blocksize,
        COMPRESS=compression,
        BIGTIFF="IF_SAFER",
        NUM_THREADS="ALL_CPUS"
    )
    with rasterio.open(src_path) as src:
        cog_translate(
            src,
            dst_path,
            profile,
            in_memory=False,
            overview_resampling=Resampling.nearest,
            overview_levels=overviews,
        )
    assert cog_validate(dst_path)
    return dst_path

def generate_quicklook(src_path: str, out_png: str, band_indices=(1,2,3)) -> str:
    with rasterio.open(src_path) as src:
        arr = src.read(band_indices)
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        arr = np.transpose(arr, (1,2,0))
        img = Image.fromarray(arr)
        img.save(out_png)
    return out_png

def apply_cloud_mask(src_path: str, out_path: str, cloud_mask_band: Optional[int] = None) -> str:
    # For Sentinel-2, use QA band or dummy mask
    with rasterio.open(src_path) as src:
        arr = src.read()
        if cloud_mask_band:
            mask = src.read(cloud_mask_band) > 0
            arr = np.where(mask, np.nan, arr)
        # else: skip
        meta = src.meta.copy()
        with rasterio.open(out_path, "w", **meta) as dst:
            dst.write(arr)
    return out_path
