from . import views
from django.urls import path, include

urlpatterns = [
    path('',views.user_home_page,name="Home")
]
