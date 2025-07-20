from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_home_page, name="Home"),
    path('user-bike-rental', views.user_bike_rental, name="user-bike-rental"),
    path('rent/', views.bike_rental_view, name='bike_rental_submit'),
    path('success/', views.success_view, name='success_page'),  # ✅ Add this line
]
