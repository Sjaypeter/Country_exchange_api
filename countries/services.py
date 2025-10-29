import requests
import random
from decimal import Decimal
from django.utils import timezone
from .models import Country, RefreshMetadata

COUNTRIES_API = "https://restcountries.com/v2/all?fields=name,capital,region,population,flag,currencies"
EXCHANGE_RATE_API = "https://open.er-api.com/v6/latest/USD"

class CountryService:
    @staticmethod
    def fetch_countries():
        try:
            response = requests.get(COUNTRIES_API, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Could not fetch data from RestCountries API: {str(e)}")

    @staticmethod
    def fetch_exchange_rates():
        try:
            response = requests.get(EXCHANGE_RATE_API, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get('rates', {})
        except requests.RequestException as e:
            raise Exception(f"Could not fetch data from Exchange Rate API: {str(e)}")

    @staticmethod
    def calculate_gdp(population, exchange_rate):
        if not exchange_rate or exchange_rate == 0:
            return None
        multiplier = random.uniform(1000, 2000)
        return Decimal(population) * Decimal(multiplier) / Decimal(exchange_rate)

    @staticmethod
    def get_currency_code(currencies):
        if not currencies or len(currencies) == 0:
            return None
        return currencies[0].get('code')

    @staticmethod
    def refresh_countries():
        countries_data = CountryService.fetch_countries()
        exchange_rates = CountryService.fetch_exchange_rates()

        updated_count = 0
        created_count = 0

        for country_data in countries_data:
            name = country_data.get('name')
            if not name:
                continue

            capital = country_data.get('capital')
            region = country_data.get('region')
            population = country_data.get('population', 0)
            flag_url = country_data.get('flag')
            currencies = country_data.get('currencies', [])

            currency_code = CountryService.get_currency_code(currencies)
            exchange_rate = None
            estimated_gdp = None

            if currency_code:
                exchange_rate = exchange_rates.get(currency_code)
                if exchange_rate:
                    estimated_gdp = CountryService.calculate_gdp(population, exchange_rate)
                else:
                    estimated_gdp = None
            else:
                estimated_gdp = Decimal('0')

            country, created = Country.objects.update_or_create(
                name__iexact=name,
                defaults={
                    'name': name,
                    'capital': capital,
                    'region': region,
                    'population': population,
                    'currency_code': currency_code,
                    'exchange_rate': exchange_rate,
                    'estimated_gdp': estimated_gdp,
                    'flag_url': flag_url,
                }
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        total = Country.objects.count()
        metadata = RefreshMetadata.get_instance()
        metadata.total_countries = total
        metadata.save()

        return {
            'total_countries': total,
            'created': created_count,
            'updated': updated_count,
            'last_refreshed_at': metadata.last_refreshed_at
        }
