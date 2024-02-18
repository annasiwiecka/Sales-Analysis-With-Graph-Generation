from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm
# Create your views here.

def home(request):
    form = SalesSearchForm(request.POST or None)

    return render(request, 'sales/home.html', {
        'form': form
    })

class SaleListView(ListView):
    model = Sale 
    template_name = 'sales/list.html'

class SaleDetailView(DetailView):
    model = Sale 
    template_name = 'sales/detail.html'