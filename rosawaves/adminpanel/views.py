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
    return_due_bookings = BikeRental.objects.filter(dropoff_date__lte=today,status="approved")
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
        booking.advance_amount=request.POST.get("advance_amount")
        booking.deposit_amount=request.POST.get("deposit_amount")
        booking.save()
        return redirect("active_bookings_page")  # go back to bookings table


from datetime import date, timedelta

def deposit_pending(request):
    Deposit_payment = BikeRental.objects.filter(status="Returned")
    return render(request, "Deposit_payment.html", {"deposit_pending": Deposit_payment})


from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages

def process_return(request, booking_id):
    # Find the booking
    booking = get_object_or_404(BikeRental, id=booking_id)

    # Example: mark booking as returned (you can customize logic)
    booking.status = "Returned"
    booking.dropoff_date=date.today()
    booking.deposit_paymet_date=date.today()+ timedelta(days=20)
    booking.save()

    # Show a success message
    messages.success(request, f"Booking for {booking.full_name} has been marked as returned.")

    # Redirect back to your return bookings page
    return redirect("return_bookings")  # make sure you have a url named 'return_bookings'

def return_bookings(request):
    return_due_bookings = BikeRental.objects.filter(status="Active")
    return render(request, "return_bookings.html", {"return_due_bookings": return_due_bookings})


from django.shortcuts import render, get_object_or_404

def generate_bill(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)

    # Example Bill Calculation (you can customize logic)
    rental_rate = 500  # example per day rent
    total_amount = booking.rental_days * rental_rate
    balance = total_amount - booking.advance_amount - booking.deposit_amount

    context = {
        "booking": booking,
        "rental_rate": rental_rate,
        "total_amount": total_amount,
        "balance": balance,
    }

    return render(request, "bill.html", context)




