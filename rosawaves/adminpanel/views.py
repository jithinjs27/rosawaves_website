from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from rosawaves_app.models import BikeRental
# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404

def admin_dashboard(request):
    pending_requests = BikeRental.objects.filter(status="pending")
    return render(request, "index_admin_page_home.html", {"pending_requests": pending_requests})


def active_bookings_function(request):
    today = date.today()
    active_bookings = BikeRental.objects.filter(pickup_date__lte=today, dropoff_date__gte=today,status="approved")
    return render(request, "active_booking.html", {"active_bookings": active_bookings})
def return_due_function(request):
    today = date.today()
    return_due_bookings = BikeRental.objects.filter(dropoff_date__lte=today)
    return render(request, "Return_due.html", {"return_due_bookings": return_due_bookings})



def approve_booking(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    booking.status = "approved"
    booking.save()
    return redirect('/admin_dashboard')  # Replace with the actual name/path of your dashboard view

def reject_booking(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    booking.status = "rejected"
    booking.save()
    return redirect('/admin_dashboard')





