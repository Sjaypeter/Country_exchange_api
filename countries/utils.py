import requests
from requests.exceptions import RequestException

# External API endpoints
COUNTRIES_API = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_API = "https://open.er-api.com/v6/latest/USD"

DEFAULT_TIMEOUT = 10  # seconds


class ExternalAPIError(Exception):
    """Custom error to handle API fetch issues."""
    def __init__(self, api_name: str, message: str = None):
        self.api_name = api_name
        self.message = message or f"Could not fetch data from {api_name}"
        super().__init__(self.message)


def fetch_countries():
    """Fetch all countries from the REST Countries API."""
    try:
        response = requests.get(COUNTRIES_API, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except RequestException:
        raise ExternalAPIError("Countries API")


def fetch_exchange_rates():
    """Fetch currency exchange rates (base USD)."""
    try:
        response = requests.get(EXCHANGE_API, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        # Ensure structure is as expected
        if data.get("result") == "success" and "rates" in data:
            return data["rates"]

        # Sometimes API shape may differ slightly
        if "rates" in data:
            return data["rates"]

        raise ExternalAPIError("Exchange Rates API")
    except RequestException:
        raise ExternalAPIError("Exchange Rates API")