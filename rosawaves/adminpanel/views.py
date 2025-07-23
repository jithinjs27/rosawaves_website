from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from rosawaves_app.models import BikeRental
# Create your views here.
def admin_dashboard(request):
    return render(request,"index_admin_page_home.html")

def active_bookings_function(request):
    today = date.today()
    active_bookings = BikeRental.objects.filter(pickup_date__lte=today, dropoff_date__gte=today)
    return render(request, "active_booking.html", {"active_bookings": active_bookings})





