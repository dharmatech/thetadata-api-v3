# Gemini Context: `thetadata-api-v3`

## Project Overview

This project is a Python client library for the ThetaData API (v3), designed to fetch financial options data. It provides a set of functions that correspond to specific API endpoints, returning the data conveniently as pandas DataFrames.

The library uses `httpx` for making streaming HTTP requests to a locally running ThetaData instance (`http://localhost:25503/v3`) and `pandas` for data manipulation.

The architecture is modular, with each API endpoint handled in its own file (e.g., `option_history_greeks_all.py`). A key feature is a caching layer implemented in the `src/thetadata_api_v3/cached/` subpackage. This caching mechanism is designed to reduce redundant API calls and includes logic to avoid caching incomplete data for the current trading day.

## Building and Running

This project is managed using `uv`.

### Installation

To install the package and its dependencies, run:

```sh
uv pip install .
```

Alternatively, it can be installed directly from its GitHub repository:

```sh
uv pip install git+https://github.com/dharmatech/thetadata-api-v3.git
```

### Running

The primary use of this project is as a library. You can import the functions into your own scripts to fetch data. 

Example:
```python
from thetadata_api_v3.cached.option_history_greeks_all import option_history_greeks_all

# Fetch cached greeks data
df = option_history_greeks_all('2025-10-29', 'GME', '2025-10-31', interval='1h')
print(df)
```

## Development Conventions

*   **Modular Design**: Each API endpoint corresponds to its own Python module in the `src/thetadata_api_v3/` directory.
*   **Caching**: A caching layer is provided in the `src/thetadata_api_v3/cached/` directory. This is the preferred way to access the API functions to avoid excessive calls.
    *   The cache directory is configurable via the `THETADATA_API_V3_PY_CACHE_DIR` environment variable. If not set, it defaults to `~/.thetadata-api-v3-cache`.
    *   The cache is automatically bypassed for the current date during market hours (before 4:00 PM ET) to prevent storing incomplete data.
*   **Dependencies**: Project dependencies are managed in `pyproject.toml` and locked with `uv.lock`.
*   **Testing**: There is no formal testing framework configured. Testing appears to be done manually via commented-out code blocks within the source files themselves.
