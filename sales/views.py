from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id

# Create your views here.

def home(request):
    sales_df = None
    positions_dt = None
    merged_df = None
    df = None
    
    form = SalesSearchForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')

        sale_queryset = Sale.objects.filter(created_at__date__lte=date_to, created_at__date__gte=date_from)
        if len(sale_queryset) > 0:
            sales_df = pd.DataFrame(sale_queryset.values())
            sales_df['customer_id'] = sales_df['customer_id'].apply(get_customer_from_id)
            sales_df['salesman_id'] = sales_df['salesman_id'].apply(get_salesman_from_id)
            sales_df['created_at'] = sales_df['created_at'].apply(lambda x: x.strftime('%d-%m-%Y'))

            sales_df.rename({'customer_id': 'customer','salesman_id': 'salesman', 'id': 'sales_id'}, axis=1, inplace=True)

            positions_data = []
            for sale in sale_queryset:
                for position in sale.get_positions():
                    obj = {
                        'position_id': position.id, 
                        'product': position.product.name,
                        'category': position.product.category,
                        'quantity': position.quantity,
                        'price': position.price,
                        'sales_id': position.get_sales_id()
                    }
                    positions_data.append(obj)

            positions_df = pd.DataFrame(positions_data)
            merged_df = pd.merge(sales_df, positions_df, on='sales_id')

            df = merged_df.groupby('transaction_id', as_index=False)['price'].agg('sum')
            df_category = merged_df.groupby('category', as_index=False)['price'].agg('sum')
            
            sales_df = sales_df.to_html()
            positions_df = positions_df.to_html()
            merged_df = merged_df.to_html()
            df = df.to_html()
            df_category = df_category.to_html()
        else:
            print('no data')
        
    return render(request, 'sales/home.html', {
        'form': form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'df_category': df_category
    })

class SaleListView(ListView):
    model = Sale 
    template_name = 'sales/list.html'

class SaleDetailView(DetailView):
    model = Sale 
    template_name = 'sales/detail.html'