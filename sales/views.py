from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm
import pandas as pd

# Create your views here.

def home(request):
    sales_df = None
    positions_dt = None
    
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sale_queryset = Sale.objects.filter(created_at__date__lte=date_to, created_at__date__gte=date_from)
        
        if len(sale_queryset) > 0:
            sales_df = pd.DataFrame(sale_queryset.values())
            positions_data = []
            for sale in sale_queryset:
                for position in sale.get_positions():
                    obj = {
                        'position_id': position.id, 
                        'product': position.product.name,
                        'category': position.product.category,
                        'quantity': position.quantity,
                        'price': position.price
                    }

                    positions_data.append(obj)

            positions_dt = pd.DataFrame(positions_data)
            
            sales_df = sales_df.to_html()
            positions_dt = positions_dt.to_html()
        else:
            print('no data')
        
    return render(request, 'sales/home.html', {
        'form': form,
        'sales_df': sales_df,
        'positions_dt': positions_dt
    })

class SaleListView(ListView):
    model = Sale 
    template_name = 'sales/list.html'

class SaleDetailView(DetailView):
    model = Sale 
    template_name = 'sales/detail.html'