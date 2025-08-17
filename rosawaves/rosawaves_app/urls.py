from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_home_page, name="Home"),
    path('user-bike-rental', views.user_bike_rental, name="user-bike-rental"),
    path('rent/', views.bike_rental_view, name='bike_rental_submit'),
    path('success/', views.success_view, name='success_page'),
    path('contact/',views.contact_view, name='contact_page'),
    path('booking_status/',views.booking_status_view, name='booking_status'),
    path("success/booking_status/", views.booking_status, name="booking_status"),
    path("success/booking_status/payment/<int:booking_id>/", views.payment_page, name="payment_page"),


]

