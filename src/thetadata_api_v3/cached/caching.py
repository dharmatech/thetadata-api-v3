import os
from pathlib import Path

custom_cache_dir = os.getenv('THETADATA_API_V3_PY_CACHE_DIR')
if custom_cache_dir:
    CACHE_DIR = Path(custom_cache_dir)
else:
    CACHE_DIR = Path.home() / ".thetadata-api-v3-cache"

CACHE_DIR.mkdir(parents=True, exist_ok=True)