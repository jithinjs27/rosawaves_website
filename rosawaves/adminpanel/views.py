from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from rosawaves_app.models import BikeRental
# Create your views here.
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from .forms import BookingForm

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



from django.shortcuts import redirect, get_object_or_404

def edit_booking(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    if request.method == "POST":
        booking.full_name = request.POST.get("full_name")
        booking.email = request.POST.get("email")
        booking.phone = request.POST.get("phone")
        booking.bike_model = request.POST.get("bike_model")
        booking.pickup_date = request.POST.get("pickup_date")
        booking.dropoff_date = request.POST.get("dropoff_date")
        booking.license_number = request.POST.get("license_number")
        booking.save()
        return redirect("active_bookings_page")  # go back to bookings table


from datetime import date, timedelta

def deposit_pending(request):
    today = date.today()
    cutoff_date = today - timedelta(days=20)

    # filter returned bookings with dropoff date older than 20 days
    deposit_booking = BikeRental.objects.filter(
        dropoff_date__lte=cutoff_date,
        status="returned"
    )

    # Debug print for matching bookings
    if deposit_booking.exists():
        print("=== DEBUG: Bookings passed 20 days and returned ===")
        for booking in deposit_booking:
            days_passed = (today - booking.dropoff_date).days
            print(f"User: {booking.full_name}, Dropoff: {booking.dropoff_date}, "
                  f"Days Passed: {days_passed}, Status: {booking.status}")
    else:
        print("=== DEBUG: No bookings found that passed 20 days with status returned ===")

    # Add days_passed for template usage
    booking_list = []
    for booking in deposit_booking:
        days_passed = (today - booking.dropoff_date).days
        booking_list.append({
            "id": booking.id,
            "full_name": booking.full_name,
            "bike_model": booking.bike_model,
            "dropoff_date": booking.dropoff_date,
            "days_passed": days_passed,
            "status": booking.status,
        })

    return render(request, "Deposit_payment.html", {"Deposit_booking": booking_list})





from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def process_return(request):
    if request.method == "POST":
        booking_id = request.POST.get("booking_id")
        # total_deposit = request.POST.get("total_deposit")
        # amount_deducted = request.POST.get("amount_deducted")
        # remarks = request.POST.get("remarks")

        # Fetch uniquely by booking id (no duplicates possible)
        booking = get_object_or_404(BikeRental, id=booking_id)

        # booking.total_deposit = total_deposit
        # booking.amount_deducted = amount_deducted
        # booking.remarks = remarks
        booking.status = "Returned"
        booking.save()

        messages.success(request, f"Return processed for {booking.full_name}")
        return redirect("return_due_bookings")

    return redirect("return_due_bookings")








