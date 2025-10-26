from django.db import models
from django.utils import timezone

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    capital = models.CharField(max_length=255, null=True, blank=True)
    region = models.CharField(max_length=255, null=True, blank=True)
    population = models.BigIntegerField()

    # Currency fields
    currency_code = models.CharField(max_length=10, null=True, blank=True)
    exchange_rate = models.FloatField(null=True, blank=True)

    estimated_gdp = models.FloatField(null=True, blank=True)
    flag_url = models.URLField(null=True, blank=True)

    last_refreshed_at = models.DateTimeField(default=timezone.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "capital": self.capital,
            "region": self.region,
            "population": self.population,
            "currency_code": self.currency_code,
            "exchange_rate": self.exchange_rate,
            "estimated_gdp": self.estimated_gdp,
            "flag_url": self.flag_url,
            "last_refreshed_at": self.last_refreshed_at.replace(microsecond=0).isoformat() + 'Z'
        }

    def __str__(self):
        return self.name