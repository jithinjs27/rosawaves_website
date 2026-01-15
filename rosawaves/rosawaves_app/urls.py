from django.urls import path
from . import views

urlpatterns = [

    # Home
    path('', views.user_home_page, name="home"),

    # Booking flow
    path('user-bike-rental/', views.user_bike_rental, name="user-bike-rental"),
    path('rent/', views.bike_rental_view, name='bike_rental_submit'),
    path('booking_options/', views.booking_options, name="booking_options"),

    # Payment flow
    path('payment/<int:booking_id>/', views.payment_page, name="payment_page"),
    path('payment/success/<int:booking_id>/', views.payment_success, name="payment_success"),

    # Booking status
    path('booking/status/', views.booking_status, name='booking_status'),

    # Static pages
    path('contact/', views.contact_view, name='contact'),
    path('invoice/<int:booking_id>/', views.download_invoice, name='download_invoice'),


    # Razorpay (only if you still use AJAX somewhere)
    path('create-order/', views.create_razorpay_order, name='create_razorpay_order'),

    path(
        "ajax/available-bikes/",
        views.ajax_available_bikes,
        name="ajax_available_bikes"
    ),

]
