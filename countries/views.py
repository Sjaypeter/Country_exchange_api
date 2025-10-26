import random
from django.http import JsonResponse
from django.utils import timezone
from django.db import transaction
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from .models import Country
from .utils import fetch_countries, fetch_exchange_rates, ExternalAPIError
import os
from django.http import FileResponse
from .image_utils import generate_summary_image
from django.conf import settings



def json_error(message, details=None, status=400):
    payload = {"error": message}
    if details:
        payload["details"] = details
    return JsonResponse(payload, status=status)


@csrf_exempt
@require_http_methods(["POST"])
def refresh_countries(request):
    """
    Fetch all countries and exchange rates, compute GDP, and store/update DB.
    Handles partial validation failures gracefully.
    Returns:
        200 - successful (even if some invalid entries skipped)
        400 - all invalid (nothing saved)
        503 - external API failure
        500 - unexpected internal error
    """
    try:
        countries_data = fetch_countries()
        rates = fetch_exchange_rates()
    except ExternalAPIError as e:
        return json_error(
            "External data source unavailable",
            details=f"Could not fetch data from {e.api_name}",
            status=503,
        )

    now = timezone.now()
    total_saved = 0
    invalid_countries = []

    try:
        with transaction.atomic():
            for c in countries_data:
                name = c.get("name")
                capital = c.get("capital")
                region = c.get("region")
                population = c.get("population")
                flag = c.get("flag")
                currencies = c.get("currencies") or []

                # ✅ Validate required fields
                if not name:
                    invalid_countries.append({"country": "(unknown)", "error": "name is required"})
                    continue
                if not population or population <= 0:
                    invalid_countries.append({"country": name, "error": "population is required"})
                    continue

                # ✅ Normalize currency code
                code = (currencies[0].get("code") or "").upper() if currencies else None
                exchange_rate = None
                estimated_gdp = None

                if not code:
                    # Currency missing → store but with 0 GDP
                    estimated_gdp = 0
                else:
                    rate = rates.get(code)
                    if rate:
                        exchange_rate = float(rate)
                        if exchange_rate > 0:
                            multiplier = random.randint(1000, 2000)
                            estimated_gdp = population * multiplier / exchange_rate
                    else:
                        exchange_rate = None
                        estimated_gdp = None

                # ✅ Insert or update record
                Country.objects.update_or_create(
                    name__iexact=name,
                    defaults={
                        "name": name,
                        "capital": capital,
                        "region": region,
                        "population": population,
                        "currency_code": code,
                        "exchange_rate": exchange_rate,
                        "estimated_gdp": estimated_gdp,
                        "flag_url": flag,
                        "last_refreshed_at": now,
                    },
                )
                total_saved += 1

        total_in_db = Country.objects.count()

        # Case 1: All invalid — nothing saved
        if total_saved == 0:
            return json_error(
                "Validation failed",
                details={"error": "No valid country data found."},
                status=400
            )

        # ✅ Generate summary image safely
        try:
            generate_summary_image()
        except Exception:
            pass

        # ✅ Always return 200 OK, even if some countries were invalid
        response_data = {
            "message": (
                "Refresh completed with some invalid entries."
                if invalid_countries else "Refresh successful"
            ),
            "total_countries_saved": total_in_db,
            "invalid_entries_count": len(invalid_countries),
            "sample_invalids": invalid_countries[:5] if invalid_countries else [],
            "last_refreshed_at": now.replace(microsecond=0).isoformat() + "Z",
        }

        return JsonResponse(response_data, status=200)

    except Exception as e:
        return json_error("Internal server error", details=str(e), status=500)



@require_GET
def get_countries(request):
    """
    GET /countries
    Optional query params:
      - ?region=Africa
      - ?currency=NGN
      - ?sort=gdp_desc
    """
    region = request.GET.get("region")
    currency = request.GET.get("currency")
    sort = request.GET.get("sort")

    qs = Country.objects.all()

    if region:
        qs = qs.filter(region__iexact=region)
    if currency:
        qs = qs.filter(currency_code__iexact=currency)
    if sort == "gdp_desc":
        qs = qs.order_by("-estimated_gdp")

    data = [country.to_dict() for country in qs]
    return JsonResponse(data, safe=False)

@csrf_exempt
@require_http_methods(["GET", "DELETE"])
def country_detail(request, name):
    """
    GET /countries/<name> → Get one country by name
    DELETE /countries/<name> → Delete a country record
    """
    try:
        country = Country.objects.get(name__iexact=name)
    except Country.DoesNotExist:
        return json_error("Country not found", status=404)

    if request.method == "GET":
        return JsonResponse(country.to_dict())

    elif request.method == "DELETE":
        country.delete()
        return JsonResponse({"message": f"{name} deleted successfully."})

@require_GET
def get_status(request):
    """GET /countries/status"""
    total = Country.objects.count()
    last = Country.objects.order_by("-last_refreshed_at").first()
    last_ts = last.last_refreshed_at.replace(microsecond=0).isoformat() + "Z" if last else None
    return JsonResponse({
        "total_countries": total,
        "last_refreshed_at": last_ts
    })

@require_http_methods(["GET"])
def get_summary_image(request):
    """
    GET /countries/image → Serve the summary image if it exists,
    otherwise return JSON error.
    """
    cache_dir = os.path.join(settings.BASE_DIR, "cache")
    image_path = os.path.join(cache_dir, "summary.png")

    if not os.path.exists(image_path):
        return json_error("Summary image not found", status=404)

    return FileResponse(open(image_path, "rb"), content_type="image/png")