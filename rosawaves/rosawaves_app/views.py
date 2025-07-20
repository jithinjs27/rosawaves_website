from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import BikeRentalForm

from django.shortcuts import render, redirect
from .models import BikeRental

# Create your views here.

def user_home_page(request):
    return render(request,"index_user_home_page.html")
def user_bike_rental(request):
    return render(request,"Bike_rental_user_form.html")


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
