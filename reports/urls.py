from django.urls import path
from .views import create_report

app_name = 'reports'

urlpatterns = [
    path('save/', create_report, name='create-report'),
]