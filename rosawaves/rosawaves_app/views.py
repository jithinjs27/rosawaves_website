from django.shortcuts import render, get_object_or_404, redirect
from .models import BikeRental
from adminpanel.models import BikeModel
from adminpanel.models import offers
from django.http import HttpResponse
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
def user_home_page(request):
    offer=offers.objects.all()
    return render(request, "index_user_home_page.html",{"offers": offer})


def user_bike_rental(request):
    bikes = BikeModel.objects.filter(Status="Available")
    return render(request, "Bike_rental_user_form.html", {"bikes": bikes})


def bike_rental_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        bike_id = request.POST.get('bike_model')  # this is a number
        rental_days = request.POST.get('rental_days', '')
        pickup_date = request.POST.get('pickup_date')
        dropoff_date = request.POST.get('dropoff_date')
        rider_pic = request.FILES.get('rider_pic')
        license_number = request.POST.get('license_number')

        # File uploads
        aadhar_upload = request.FILES.get('aadhar_upload', None)
        passport_upload = request.FILES.get('passport_upload', None)
        hotel_upload = request.FILES.get('hotel_upload', None)
        total_bill_amount=request.POST.get("total_bill_amount")
        # Fetch actual bike
        bike = BikeModel.objects.get(id=bike_id)

        # Save booking
        BikeRental.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            bike_model=bike.name,  # storing name (your model uses CharField)
            rental_days=rental_days,
            pickup_date=pickup_date,
            dropoff_date=dropoff_date,
            rider_pic=rider_pic,
            license_number=license_number,
            aadhar_upload=aadhar_upload,
            # If you add these fields in model later:
            passport_upload=passport_upload,
            hotel_upload=hotel_upload,
            total_bill_amount=total_bill_amount,
            bike_number=bike.Vehicle_number

        )
        return redirect('success_page')

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


def payment_page(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    return render(request, "payment.html", {"booking": booking})

def booking_options(request):
    return render(request,"Booking_option_page.html")

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
