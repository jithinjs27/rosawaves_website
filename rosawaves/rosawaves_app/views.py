from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BikeRentalForm
from adminpanel.models import BikeModel

from django.shortcuts import render, redirect
from .models import BikeRental

# Create your views here.

def user_home_page(request):
    return render(request,"index_user_home_page.html")
def user_bike_rental(request):
    bikes = BikeModel.objects.all()
    return render(request,"Bike_rental_user_form.html",{"bikes": bikes})


def bike_rental_view(request):
    if request.method == 'POST':
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone = request.POST['phone']
        bike_model = request.POST['bike_model']
        rental_days = request.POST['rental_days']
        pickup_date = request.POST['pickup_date']
        dropoff_date = request.POST['dropoff_date']
        rider_pic = request.FILES['rider_pic']
        license_number = request.POST['license_number']
        aadhar_upload = request.FILES['aadhar_upload']

        # Save to the database
        BikeRental.objects.create(
            full_name=full_name,
            email=email,
            phone=phone,
            bike_model=bike_model,
            rental_days=rental_days,
            pickup_date=pickup_date,
            dropoff_date=dropoff_date,
            rider_pic=rider_pic,
            license_number=license_number,
            aadhar_upload=aadhar_upload
        )
        return redirect('success_page')  # Change to your actual success URL or name
    return render(request, 'Bike_rental_user_form.html')  # Replace with actual template name

def success_view(request):
    return render(request, 'success.html')

def contact_view(request):
    return render(request,"User_contact_page.html")
def booking_status_view(request):
    return render(request,"booking_status.html")

def booking_status(request):
    query = request.GET.get("q", "")  # Get search input
    bookings = []

    if query:
        bookings = BikeRental.objects.filter(
            email__icontains=query
        ) | BikeRental.objects.filter(id__icontains=query)  # adjust if booking ID field is different

    return render(request, "booking_status.html", {"bookings": bookings, "query": query})

def payment_page(request, booking_id):
    booking = get_object_or_404(BikeRental, id=booking_id)
    return render(request, "payment.html", {"booking": booking})


