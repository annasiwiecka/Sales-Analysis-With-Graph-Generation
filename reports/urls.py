from django.urls import path
from .views import *

app_name = "reports"

urlpatterns = [
    path("", ReportListView.as_view(), name="list"),
    path("save/", create_report, name="create-report"),
    path("upload/", csv_upload, name='upload'),
    path('from_file/', UploadTemplateView.as_view(), name='from-file'),
    path("<pk>/", ReportDetailView.as_view(), name="detail"),
    path("<pk>/pdf/", render_pdf_view, name="pdf"),
]
