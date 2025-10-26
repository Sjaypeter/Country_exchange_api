from django.urls import path
from . import views

urlpatterns = [
    path("countries/refresh", views.refresh_countries, name="refresh_countries"),  # POST
    path("countries", views.get_countries, name="get_countries"),                  # GET all
    path("status", views.get_status, name="get_status"),                 # GET status
    path("countries/image", views.get_summary_image, name="get_summary_image"), # GET summary image
    path("countries/<str:name>", views.country_detail, name="country_detail"),  # GET + DELETE
]