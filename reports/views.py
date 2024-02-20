from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic import ListView, DetailView

from .utils import get_report_image
from profiles.models import Profile
from .models import Report

# Create your views here.


class ReportListView(ListView):
    model = Report
    template_name = 'reports/list.html'


class ReportDetailView(DetailView):
    model = Report
    template_name = 'reports/detail.html'


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
