# WP Engine API Python SDK

A Python SDK for interacting with the WP Engine API, enabling Python developers to programmatically interact with WP Engine services.

> **Note**: This SDK is maintained by Jeremy Pollock (jeremy.pollock@wpengine.com) and is not affiliated with or supported by WP Engine.

## Installation

```bash
pip install wp-engine-api
```

## Authentication

The SDK supports two methods of authentication:

### 1. Direct Username/Password

```python
from wp_engine_api import WPEngineAPI

# Initialize with credentials directly
client = WPEngineAPI(
    username="your-username",
    password="your-password"
)
```

### 2. Environment Variables

Create a `.env` file in your project root:
```bash
WP_ENGINE_API_USERNAME=your-username
WP_ENGINE_API_PASSWORD=your-password
```

Or set environment variables directly:
```bash
export WP_ENGINE_API_USERNAME=your-username
export WP_ENGINE_API_PASSWORD=your-password
```

Then initialize the client:
```python
from wp_engine_api import WPEngineAPI

# Initialize using environment variables
client = WPEngineAPI()
```

## Quick Start

```python
from wp_engine_api import WPEngineAPI

# Initialize the client
client = WPEngineAPI(
    username="your-username",
    password="your-password"
)

# List all sites
sites = client.sites.list()
for site in sites:
    print(f"Site: {site.name} ({site.id})")

# Get a specific site
site = client.sites.get("site_id")

# Create a backup
backup = client.backups.create(
    "site_id",
    {
        "description": "Pre-deployment backup",
        "notification_emails": ["admin@example.com"]
    }
)
```

## Features

- Full coverage of the WP Engine API
- Type hints for better IDE support
- Automatic rate limiting
- Request validation
- Comprehensive error handling
- Environment variable support
- .env file support

## Examples

### Site Management

```python
# List all sites
sites = client.sites.list()

# Get a specific site
site = client.sites.get("site_id")

# Update a site
updated_site = client.sites.update(
    "site_id",
    {"name": "New Site Name"}
)
```

### Backup Management

```python
# Create a backup
backup = client.backups.create(
    "site_id",
    {
        "description": "Pre-deployment backup",
        "notification_emails": ["admin@example.com"]
    }
)

# List backups
backups = client.backups.list("site_id")

# Get backup status
backup_status = client.backups.get("site_id", "backup_id")
```

### Error Handling

```python
from wp_engine_api.exceptions import (
    AuthenticationError,
    ValidationError,
    ResourceNotFoundError,
    RateLimitError
)

try:
    sites = client.sites.list()
except AuthenticationError:
    print("Invalid credentials")
except ResourceNotFoundError:
    print("Resource not found")
except RateLimitError as e:
    print(f"Rate limit exceeded. Retry after {e.retry_after} seconds")
except ValidationError as e:
    print(f"Invalid request: {e}")
```

## Rate Limiting

The SDK includes automatic rate limiting to help you stay within the API's limits. You can configure the rate limiting behavior:

```python
client = WPEngineAPI(
    username="your-username",
    password="your-password",
    max_retries=3,
    retry_delay=1.0
)
```

## Development

### Setup Development Environment

1. Clone the repository:
```bash
git clone https://github.com/wpengine/wp-engine-api-python.git
cd wp-engine-api-python
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install development dependencies:
```bash
pip install -r requirements.txt
```

### Running Tests

```bash
pytest
```

### Generating API Client

The SDK uses OpenAPI Generator to generate the base API client code. To regenerate the client:

```bash
python scripts/generate_client.py
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Maintainer

This SDK is maintained by Jeremy Pollock (jeremy.pollock@wpengine.com). For any questions, issues, or contributions, please reach out directly.
