from django.shortcuts import render, get_object_or_404, redirect
from .models import BikeRental
from adminpanel.models import BikeModel
from adminpanel.models import offers
from django.http import HttpResponse
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from django.shortcuts import render, redirect
from django.contrib import messages
import razorpay

def user_home_page(request):
    offer = offers.objects.all()
    return render(request, "index_user_home_page.html", {"offers": offer})


def user_bike_rental(request):
    # Get only available bikes
    bikes = BikeModel.objects.filter(Status="Available")

    # Add price_category attribute for filtering in template
    for bike in bikes:
        if bike.rent_per_day <= 500:
            bike.price_category = "low"
        elif bike.rent_per_day <= 1000:
            bike.price_category = "medium"
        else:
            bike.price_category = "high"

    return render(request, "Bike_rental_user_form.html", {"bikes": bikes})


from django.shortcuts import redirect, get_object_or_404

def bike_rental_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bike_id = request.POST.get('bike_model')
        rental_days = request.POST.get('rental_days', '')
        pickup_date = request.POST.get('pickup_date')
        dropoff_date = request.POST.get('dropoff_date')
        rider_pic = request.FILES.get('rider_pic')
        license_number = request.POST.get('license_number')

        aadhar_upload = request.FILES.get('aadhar_upload')
        passport_upload = request.FILES.get('passport_upload')
        hotel_upload = request.FILES.get('hotel_upload')
        total_bill_amount = request.POST.get("total_bill_amount")

        # Fetch bike safely
        bike = get_object_or_404(BikeModel, id=bike_id)

        # ✅ SAVE & CAPTURE BOOKING
        booking = BikeRental.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            bike_model=bike.name,
            rental_days=rental_days,
            pickup_date=pickup_date,
            dropoff_date=dropoff_date,
            rider_pic=rider_pic,
            license_number=license_number,
            aadhar_upload=aadhar_upload,
            passport_upload=passport_upload,
            hotel_upload=hotel_upload,
            total_bill_amount=total_bill_amount,
            bike_number=bike.Vehicle_number,
            status="pending"   # recommended
        )

        return redirect('payment_page', booking_id=booking.id)

    bikes = BikeModel.objects.all()
    return render(request, 'Bike_rental_user_form.html', {"bikes": bikes})



def success_view(request):
    return render(request, 'success.html')


def contact_view(request):
    return render(request, "User_contact_page.html")


def booking_status_view(request):
    return render(request, "booking_status.html")


def booking_status(request):
    query = request.GET.get("q", "")
    bookings = []

    if query:
        bookings = BikeRental.objects.filter(
            email__icontains=query
        ) | BikeRental.objects.filter(id__icontains=query)

    return render(request, "booking_status.html", {"bookings": bookings, "query": query})


# def payment_page(request, booking_id):
#     booking = get_object_or_404(BikeRental, id=booking_id)
#     return render(request, "payment.html", {"booking": booking})


def booking_options(request):
    return render(request, "Booking_option_page.html")


client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)


@csrf_exempt
def create_razorpay_order(request):
    if request.method == "POST":
        amount = int(request.POST.get("amount"))

        order = client.order.create({
            "amount": amount,
            "currency": "INR",
            "payment_capture": "1"
        })

        return JsonResponse(order)


def proceed_to_payment(request):
    if request.method == "POST":
        booking = BikeRental.objects.create(
            full_name=request.POST["full_name"],
            email=request.POST["email"],
            phone=request.POST["phone"],
            bike_id=request.POST["bike_model"],
            pickup_date=request.POST["pickup_date"],
            dropoff_date=request.POST["dropoff_date"],
            total_bill_amount=request.POST["total_bill_amount"],
            status="pending",
            payment_status="initiated"
        )


        return redirect("payment_page", booking_id=booking.id)




def payment_page(request, booking_id):
    try:
        with transaction.atomic():
            # Lock the booking row
            booking = BikeRental.objects.select_for_update().get(id=booking_id)

            # Lock the bike row
            bike = BikeModel.objects.select_for_update().get(Vehicle_number=booking.bike_number)

            # Check availability AGAIN (inside transaction)
            if bike.Status != "Available":
                messages.error(request, "Sorry! This bike was just booked by another user.")
                return redirect("user-bike-rental")

            # Razorpay client
            client = razorpay.Client(
                auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
            )

            order = client.order.create({
                "amount": int(booking.total_bill_amount * 100),
                "currency": "INR",
                "payment_capture": 1
            })

            # Save Razorpay Order ID
            booking.razorpay_order_id = order["id"]
            booking.save()

        return render(request, "payment.html", {
            "booking": booking,
            "order_id": order["id"],
            "razorpay_key": settings.RAZORPAY_KEY_ID
        })

    except BikeRental.DoesNotExist:
        messages.error(request, "Invalid booking.")
        return redirect("home")

    except BikeModel.DoesNotExist:
        messages.error(request, "Bike not found.")
        return redirect("home")



def payment_success(request, booking_id):
    booking = BikeRental.objects.get(id=booking_id)
    booking.payment_status = "paid"
    booking.razorpay_payment_id = request.GET.get("pid")
    booking.save()

    return render(request, "success.html", {"booking": booking})
