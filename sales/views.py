from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm
import pandas as pd

# Create your views here.

def home(request):
    sales_df = None
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        queryset = Sale.objects.filter(created_at__date__lte=date_to, created_at__date__gte=date_from)
        
        if len(queryset) > 0:
            sales_df = pd.DataFrame(queryset.values())
            sales_df = sales_df.to_html()
        else:
            print('no data')
        
    return render(request, 'sales/home.html', {
        'form': form,
        'sales_df': sales_df
    })

class SaleListView(ListView):
    model = Sale 
    template_name = 'sales/list.html'

class SaleDetailView(DetailView):
    model = Sale 
    template_name = 'sales/detail.html'