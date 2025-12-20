from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("", views.dashboard, name="dashboard"),  # dashboard = homepage
    path("scan/", views.index, name="index"),
    path("result/<int:scan_id>/", views.scan_result, name="scan_result"),
    path("webcam-scan/", views.webcam_scan, name="webcam_scan"),
   
    path("history/", views.history, name="history"),
]
