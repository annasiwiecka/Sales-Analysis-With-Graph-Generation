from django.urls import path 

from .views import * 

app_name = 'sales'

urlpatterns = [
    path('', home, name='home'),
    path('sales/', SaleListView.as_view(), name='list'),
    path('sales/<pk>/', SaleDetailView.as_view(), name='detail')
]