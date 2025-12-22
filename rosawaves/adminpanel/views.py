from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from rosawaves_app.models import BikeRental, BikeModel
from .models import offers
from django.shortcuts import render, redirect
from django.db import IntegrityError
from .models import BikeModel,accessories
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from .models import BikeModel
# -------------------------
# Dashboard
# -------------------------
def admin_dashboard(request):
    pending_requests = BikeRental.objects.filter(status="pending")
    return render(request, "index_admin_page_home.html", {"pending_requests": pending_requests})


# -------------------------
# Active Bookings
# -------------------------
def active_bookings_function(request):
    now = datetime.now()

    active_bookings = BikeRental.objects.filter(
        # pickup_date__lte=now,
        dropoff_date__gte=now,
        status="approved"
    )
    helmets = accessories.objects.all()

    return render(request, "active_booking.html", {"active_bookings": active_bookings,"helmets": helmets})


# -------------------------
# Return Due Bookings
# -------------------------
def return_due_function(request):
    now = datetime.now()
    return_due_bookings = BikeRental.objects.filter(
        dropoff_date__lte=now,
        status="approved"
    )
    return render(request, "Return_due.html", {"return_due_bookings": return_due_bookings})


# -------------------------
# Approve / Reject
# -------------------------
def approve_booking(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    booking.status = "approved"
    booking.save()
    bike_status_update = get_object_or_404(BikeModel, Vehicle_number=booking.bike_number)
    bike_status_update.Status = "Rented"
    bike_status_update.available_date=booking.dropoff_date
    bike_status_update.save()
    messages.success(request, f"Booking for {booking.full_name} has been approved.")
    return redirect("admin_dashboard")


def reject_booking(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    booking.status = "rejected"
    booking.save()
    messages.warning(request, f"Booking for {booking.full_name} has been rejected.")
    return redirect("admin_dashboard")


# -------------------------
# Edit Booking
# -------------------------
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
        booking.advance_amount = request.POST.get("advance_amount") or 0
        booking.deposit_amount = request.POST.get("deposit_amount") or 0
        booking.helmet_1=request.POST.get("helmet_1")
        booking.helmet_2=request.POST.get("helmet_2")
        booking.save()
        messages.success(request, f"Booking for {booking.full_name} has been updated.")
        return redirect("active_bookings_page")

    return render(request, "edit_booking.html", {"booking": booking})


# -------------------------
# Deposit Pending
# -------------------------
def deposit_pending(request):
    # Fetch bookings that are returned (but deposit not settled)
    deposit_pending_bookings = BikeRental.objects.filter(status="Returned")

    return render(request, "Deposit_payment.html", {
        "deposit_pending_bookings": deposit_pending_bookings
    })


# -------------------------
# Process Return
# -------------------------
def process_return(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    booking.status = "Returned"
    booking.save()
    bike_status_update = get_object_or_404(BikeModel, Vehicle_number=booking.bike_number)
    bike_status_update.Status = "Available"
    bike_status_update.available_date=datetime.now()
    bike_status_update.save()
    messages.success(request, f"Booking for {booking.full_name} has been marked as Returned.")
    return redirect("return_bookings")


def return_bookings(request):
    return_due_bookings = BikeRental.objects.filter(status="approved")
    return render(request, "return_bookings.html", {"return_due_bookings": return_due_bookings})


# -------------------------
# Generate Bill
# -------------------------
def generate_bill(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)

    # Example Bill Calculation
    rental_rate = 500  # per day
    try:
        rental_days = int(booking.rental_days)
    except Exception:
        rental_days = 0

    total_amount = rental_days * rental_rate
    balance = total_amount - booking.advance_amount - booking.deposit_amount

    context = {
        "booking": booking,
        "rental_rate": rental_rate,
        "rental_days": rental_days,
        "total_amount": total_amount,
        "balance": balance,
    }

    return render(request, "bill.html", context)


def offers_fun(request):
    if request.method == 'POST':
        # Handle delete request
        if 'delete_offer' in request.POST:
            offer_id = request.POST.get('delete_offer')
            offer = get_object_or_404(offers, id=offer_id)
            offer.delete()
            return redirect('offers')  # Redirect to refresh page

        # Handle upload request
        image = request.FILES.get('offerImage')
        description = request.POST.get('offerDescription', '').strip()

        if not image or not description:
            all_offers = offers.objects.all()
            return render(request, 'offers.html', {
                'error': 'Please upload an image and enter a description.',
                'offers': all_offers
            })

        offers.objects.create(offer_image=image, description=description)
        return redirect('offers')

    # Show current offers
    all_offers = offers.objects.all()
    return render(request, 'offers.html', {'offers': all_offers})






def vehicle_create(request):
    error = None
    edit_vehicle = None

    # EDIT MODE
    if "edit_id" in request.GET:
        edit_vehicle = get_object_or_404(BikeModel, id=request.GET.get("edit_id"))

    if request.method == "POST":
        try:
            vehicle_id = request.POST.get("vehicle_id")

            if vehicle_id:
                # UPDATE
                bike = get_object_or_404(BikeModel, id=vehicle_id)
                bike.name = request.POST.get("name")
                bike.Vehicle_number = request.POST.get("Vehicle_number")
                bike.mileage = request.POST.get("mileage")
                bike.rent_per_day = request.POST.get("rent_per_day")
                bike.Onwer_name = request.POST.get("Onwer_name")
                bike.Status = request.POST.get("Status")

                if request.FILES.get("bike_image"):
                    bike.bike_image = request.FILES.get("bike_image")

                bike.save()

            else:
                # CREATE
                BikeModel.objects.create(
                    name=request.POST.get("name"),
                    Vehicle_number=request.POST.get("Vehicle_number"),
                    mileage=request.POST.get("mileage"),
                    rent_per_day=request.POST.get("rent_per_day"),
                    Onwer_name=request.POST.get("Onwer_name"),
                    Status=request.POST.get("Status"),
                    bike_image=request.FILES.get("bike_image")
                )

            return redirect("vehicle_create")

        except IntegrityError:
            error = "Vehicle number already exists!"

    vehicles = BikeModel.objects.all()
    return render(request, "Vehicle_detailes.html", {
        "vehicle": vehicles,
        "error": error,
        "edit_vehicle": edit_vehicle
    })


def vehicle_delete(request, id):
    bike = get_object_or_404(BikeModel, id=id)
    bike.delete()
    return redirect("vehicle_create")


# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import accessories

def helmet_accessories(request):
    helmets = accessories.objects.all()
    edit_item = None

    if request.method == "POST":
        acc_id = request.POST.get("acc_id")
        helmet_id = request.POST.get("helmet_id")
        helmet_name = request.POST.get("helmet_name")
        status = request.POST.get("status")

        if acc_id:  # UPDATE
            item = accessories.objects.get(id=acc_id)
            item.Helmet_Id = helmet_id
            item.Helmet_name = helmet_name
            item.status = status
            item.save()
        else:  # ADD
            accessories.objects.create(
                Helmet_Id=helmet_id,
                Helmet_name=helmet_name,
                status=status
            )
        return redirect("helmet_accessories")

    # Edit
    if "edit" in request.GET:
        edit_item = get_object_or_404(accessories, id=request.GET.get("edit"))

    # Delete
    if "delete" in request.GET:
        accessories.objects.filter(id=request.GET.get("delete")).delete()
        return redirect("helmet_accessories")

    return render(request, "accessories.html", {
        "helmets": helmets,
        "edit_item": edit_item
    })



