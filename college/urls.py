from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("placements/", views.placements, name="placements"),
    path("hostel/", views.hostel, name="hostel"),
    path("contact/", views.contact, name="contact"),
]
