from django.urls import path 
from .views import * 

app_name = 'profiles'

urlpatterns = [
    path('', my_profile, name='my')
]
