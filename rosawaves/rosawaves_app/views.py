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

        alternate_ph = request.POST.get('alternate_ph')
        emergency_ph = request.POST.get('emergency_ph')
        upid = request.POST.get('upid')

        bike_id = request.POST.get('bike_model')
        rental_days = request.POST.get('rental_days')
        pickup_date = request.POST.get('pickup_date')
        dropoff_date = request.POST.get('dropoff_date')

        rider_pic = request.FILES.get('rider_pic')
        license_number = request.POST.get('license_number')

        aadhar_upload = request.FILES.get('aadhar_upload')
        passport_upload = request.FILES.get('passport_upload')
        hotel_upload = request.FILES.get('hotel_upload')

        total_bill_amount = request.POST.get("total_bill_amount")

        bike = get_object_or_404(BikeModel, id=bike_id)

        booking = BikeRental.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            alternate_ph=alternate_ph,
            emergency_ph=emergency_ph,
            upid=upid,

            bike_model=bike.name,
            bike_number=bike.Vehicle_number,

            rental_days=rental_days,
            pickup_date=pickup_date,
            dropoff_date=dropoff_date,

            rider_pic=rider_pic,
            license_number=license_number,

            aadhar_upload=aadhar_upload,
            passport_upload=passport_upload,
            hotel_upload=hotel_upload,

            total_bill_amount=total_bill_amount,
            payment_status="pending",
            status="pending"
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


from django.db.models import Q


def booking_status(request):
    query = request.GET.get("q", "").strip()
    bookings = BikeRental.objects.none()

    if query:
        if query.isdigit():
            bookings = BikeRental.objects.filter(id=int(query))
        else:
            bookings = BikeRental.objects.filter(
                Q(email__icontains=query)
            )

    return render(
        request,
        "booking_status.html",
        {"bookings": bookings, "query": query}
    )


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
            # Check availability AGAIN (inside transaction)

            if booking.payment_status == "paid":
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


from django.http import JsonResponse
from django.db.models import Q

from .models import BikeModel, BikeRental

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.db.models import Q

from django.http import JsonResponse
from django.utils.dateparse import parse_datetime
from django.utils.timezone import make_aware
from django.db.models import Q


def ajax_available_bikes(request):
    pickup_str = request.GET.get("pickup_date")
    dropoff_str = request.GET.get("dropoff_date")

    if not pickup_str or not dropoff_str:
        return JsonResponse([], safe=False)

    pickup = parse_datetime(pickup_str)
    dropoff = parse_datetime(dropoff_str)

    if not pickup or not dropoff:
        return JsonResponse([], safe=False)

    # Make timezone aware
    if pickup.tzinfo is None:
        pickup = make_aware(pickup)
    if dropoff.tzinfo is None:
        dropoff = make_aware(dropoff)

    # 🔴 Bikes already booked in selected period
    booked_bike_numbers = BikeRental.objects.filter(
        pickup_date__lt=dropoff,
        dropoff_date__gt=pickup,
        status__in=["pending", "approved"]
    ).values_list("bike_number", flat=True)

    # ✅ Available bikes = all bikes EXCEPT booked ones
    bikes = BikeModel.objects.exclude(
        Vehicle_number__in=booked_bike_numbers
    )

    data = [
        {
            "id": bike.id,
            "name": bike.name,
            "bike_number": bike.Vehicle_number,
            "rent": bike.rent_per_day,
            "image": bike.bike_image.url if bike.bike_image else "",
        }
        for bike in bikes
    ]

    return JsonResponse(data, safe=False)


from datetime import datetime


def parse_datetime_safe(value):
    if not value:
        return None

    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"):
        try:
            return datetime.strptime(value, fmt)
        except ValueError:
            pass

    return None


from django.http import HttpResponse
from reportlab.pdfgen import canvas
from .models import BikeRental


def download_invoice(request, booking_id):
    booking = BikeRental.objects.get(id=booking_id)
    bike = BikeModel.objects.get(Vehicle_number=booking.bike_number)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="invoice_{booking.id}.pdf"'

    p = canvas.Canvas(response)

    p.setFont("Helvetica-Bold", 16)
    p.drawString(200, 800, "Rosa Waves Bike Rental")

    p.setFont("Helvetica", 12)
    p.drawString(50, 760, f"Invoice ID: UK-{booking.id}")
    p.drawString(50, 740, f"Payment Status: {booking.payment_status}")

    p.drawString(50, 680, f"Customer Name: {booking.full_name}")
    p.drawString(50, 660, f"Bike: {bike.name}")
    p.drawString(50, 640, f"Rental Date: {booking.pickup_date} to {booking.dropoff_date}")
    p.drawString(50, 620, f"Total Amount: ₹{booking.total_bill_amount}")

    p.drawString(50, 580, "Thank you for choosing Rosa Waves!")

    p.showPage()
    p.save()

    return response
