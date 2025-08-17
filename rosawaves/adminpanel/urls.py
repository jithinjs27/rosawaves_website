from django.urls import path
from . import views

urlpatterns = [
    path('admin_dashboard', views.admin_dashboard, name="Admin_home_page"),
    path('active_bookings', views.active_bookings_function, name="active_bookings_page"),
    path('return_due_bookings', views.return_due_function, name="return_due_bookings_page"),
    path('approve/<int:booking_id>/', views.approve_booking, name='approve_booking'),
    path('reject/<int:booking_id>/', views.reject_booking, name='reject_booking'),
    path('bookings/<int:booking_id>/edit/', views.edit_booking, name='edit_booking'),
    path('deposit-pending', views.deposit_pending, name='deposit_pending'),
    path("return-bookings/", views.return_bookings, name="return_bookings"),
    path("return/<int:booking_id>/", views.process_return, name="process_return"),
    path("generate-bill/<int:booking_id>/", views.generate_bill, name="generate_bill"),

]
