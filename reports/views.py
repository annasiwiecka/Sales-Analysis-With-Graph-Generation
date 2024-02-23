from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView, TemplateView
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
import csv
from django.utils.dateparse import parse_date

from .utils import get_report_image
from products.models import Product
from profiles.models import Profile
from .models import Report
from customers.models import Customer
from sales.models import Sale, Position, CSV

# Create your views here.


class ReportListView(ListView):
    model = Report
    template_name = "reports/list.html"


class ReportDetailView(DetailView):
    model = Report
    template_name = "reports/detail.html"


class UploadTemplateView(TemplateView):
    template_name = "reports/from_file.html"


def csv_upload(request):
    if request.method == "POST":
        csv_file_name = request.FILES.get("file").name
        csv_file = request.FILES.get("file")
        obj, created = CSV.objects.get_or_create(file_name=csv_file_name)

        if created:
            obj.csv_file = csv_file
            obj.save()
            with open(obj.csv_file.path, "r") as f:
                reader = csv.reader(f)
                reader.__next__()
                for row in reader:

                    transaction_id = row[1]
                    product = row[2]
                    category = row[3]
                    quantity = int(row[4])
                    customer = row[5]
                    date = parse_date(row[6])

                    try:
                        product_obj = Product.objects.get(name=product, category=category)
                    except Product.DoesNotExist:
                        product_obj = None

                    if product_obj is not None:
                        customer_obj, _ = Customer.objects.get_or_create(name=customer)
                        salesman_obj = Profile.objects.get(user=request.user)
                        position_obj = Position.objects.create(
                            product=product_obj,
                            quantity=quantity,
                            created_at=date,
                        )

                        sale_obj, _ = Sale.objects.get_or_create(
                            transaction_id=transaction_id,
                            customer=customer_obj,
                            salesman=salesman_obj,
                            created_at=date,
                        )
                        sale_obj.positions.add(position_obj)
                        sale_obj.save()

    return HttpResponse()


def create_report(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        name = request.POST.get("name")
        remarks = request.POST.get("remarks")
        image = request.POST.get("image")

        img = get_report_image(image)

        author = Profile.objects.get(user=request.user)
        Report.objects.create(name=name, remarks=remarks, image=img, author=author)
        return JsonResponse({"msg": "send"})
    return JsonResponse({})


def render_pdf_view(request, pk):
    template_path = "reports/pdf.html"
    obj = get_object_or_404(Report, pk=pk)
    context = {"obj": obj}
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type="application/pdf")
    # if download
    # response["Content-Disposition"] = 'attachment; filename="report.pdf"'
    # if display
    response["Content-Disposition"] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")
    return response
