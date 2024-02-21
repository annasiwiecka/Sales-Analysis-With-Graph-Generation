from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa


from .utils import get_report_image
from profiles.models import Profile
from .models import Report

# Create your views here.


class ReportListView(ListView):
    model = Report
    template_name = "reports/list.html"


class ReportDetailView(DetailView):
    model = Report
    template_name = "reports/detail.html"


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
