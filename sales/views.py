from django.shortcuts import render
from django.views.generic import ListView, DetailView

from .models import Sale
from .forms import SalesSearchForm
from reports.forms import ReportForm
import pandas as pd
from .utils import get_customer_from_id, get_salesman_from_id, get_graph, get_chart

# Create your views here.

def home(request):
    sales_df = None
    positions_df = None
    merged_df = None
    df = None
    df_category = None
    chart = None
    
    form = SalesSearchForm(request.POST or None)
    report_form = ReportForm(request.POST or None)
    if request.method == 'POST':
        date_from = request.POST.get('date_from')
        date_to = request.POST.get('date_to')
        chart_type = request.POST.get('chart_type')
        results_by = request.POST.get('results_by')

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
            
            chart = get_chart(chart_type, merged_df, results_by)

            sales_df = sales_df.to_html(classes="table")
            positions_df = positions_df.to_html(classes="table")
            merged_df = merged_df.to_html(classes="table")
            df = df.to_html(classes="table")
            df_category = df_category.to_html(classes="table")
        else:
            print('no data')
        
    return render(request, 'sales/home.html', {
        'form': form,
        'report_form': report_form,
        'sales_df': sales_df,
        'positions_df': positions_df,
        'merged_df': merged_df,
        'df': df,
        'df_category': df_category,
        'chart': chart,
    })

class SaleListView(ListView):
    model = Sale 
    template_name = 'sales/list.html'

class SaleDetailView(DetailView):
    model = Sale 
    template_name = 'sales/detail.html'