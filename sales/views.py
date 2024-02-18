from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm
# Create your views here.

def home(request):
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

    return render(request, 'sales/home.html', {
        'form': form
    })

class SaleListView(ListView):
    model = Sale 
    template_name = 'sales/list.html'

class SaleDetailView(DetailView):
    model = Sale 
    template_name = 'sales/detail.html'