from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard', views.admin_dashboard, name="Admin_home_page"),
    path('active_bookings', views.active_bookings_function, name="active_bookings_page"),

]
