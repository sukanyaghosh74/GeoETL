import os
from eodag import EODataAccessGateway
from eodag.utils import get_timestamp
from typing import List, Dict, Any
import shutil
import logging

class EODAGClient:
    def __init__(self, config_path: str, provider: str = None):
        self.dag = EODataAccessGateway(config_path)
        if provider:
            self.dag.set_preferred_provider(provider)

    def search(self, aoi_geojson: dict, start: str, end: str, collection: str, cloud: float = None) -> List[Dict[str, Any]]:
        search_criteria = {
            "geom": aoi_geojson,
            "start": start,
            "end": end,
            "productType": collection,
        }
        if cloud is not None:
            search_criteria["cloudCover"] = f"[0,{cloud}]"
        products = self.dag.search(**search_criteria)
        return [p.properties for p in products]

    def download(self, product_ids: List[str], output_dir: str, use_mock: bool = False) -> List[str]:
        os.makedirs(output_dir, exist_ok=True)
        downloaded = []
        if use_mock:
            # Copy from sample_data/tiny.tif for each product_id
            for pid in product_ids:
                dst = os.path.join(output_dir, f"{pid}.tif")
                shutil.copy("sample_data/tiny.tif", dst)
                downloaded.append(dst)
            return downloaded
        for pid in product_ids:
            try:
                product = self.dag.get_product_by_id(pid)
                path = self.dag.download(product, outputs_prefix=output_dir)
                downloaded.append(path)
            except Exception as e:
                logging.error(f"Download failed for {pid}: {e}")
        return downloaded

# Singleton for app
from backend.app.core.config import settings
eodag_client = EODAGClient(settings.EODAG_CONFIG_PATH)
