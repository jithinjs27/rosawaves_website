from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def user_home_page(request):
    return render(request,"index_user_home_page.html")
