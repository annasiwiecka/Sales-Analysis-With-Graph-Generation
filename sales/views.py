from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
# Create your views here.

def home(request):
    return render(request, 'sales/home.html', {})

class SaleListView(ListView):
    model = Sale 
    template_name = 'sales/list.html'

class SaleDetailView(DetailView):
    model = Sale 
    template_name = 'sales/detail.html'