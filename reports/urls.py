from django.urls import path
from .views import *

app_name = "reports"

urlpatterns = [
    path("", ReportListView.as_view(), name="list"),
    path("save/", create_report, name="create-report"),
    path("<pk>/", ReportDetailView.as_view(), name="detail"),
    path("<pk>/pdf/", render_pdf_view, name="pdf"),
]
