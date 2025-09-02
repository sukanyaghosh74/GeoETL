import numpy as np
import rasterio
from typing import Dict, Any, Optional

def compute_stats(src_path: str, aoi_mask: Optional[np.ndarray] = None) -> Dict[str, Any]:
    with rasterio.open(src_path) as src:
        arr = src.read(1)
        if aoi_mask is not None:
            arr = arr[aoi_mask]
        arr = arr[~np.isnan(arr)]
        stats = {
            "mean": float(np.mean(arr)),
            "median": float(np.median(arr)),
            "std": float(np.std(arr)),
            "min": float(np.min(arr)),
            "max": float(np.max(arr)),
            "px_count": int(arr.size),
        }
        return stats

def compute_ndvi(src_path: str, red_band: int, nir_band: int, aoi_mask: Optional[np.ndarray] = None) -> Dict[str, Any]:
    with rasterio.open(src_path) as src:
        red = src.read(red_band).astype(float)
        nir = src.read(nir_band).astype(float)
        ndvi = (nir - red) / (nir + red + 1e-6)
        if aoi_mask is not None:
            ndvi = ndvi[aoi_mask]
        ndvi = ndvi[~np.isnan(ndvi)]
        return {
            "ndvi_mean": float(np.mean(ndvi)),
            "ndvi_std": float(np.std(ndvi)),
        }
