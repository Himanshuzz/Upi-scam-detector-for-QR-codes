from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django import forms
from django.core.files.storage import default_storage
from django.contrib import messages
from django.db.models import Count
from django.http import JsonResponse


from .forms import QRUploadForm
from .models import QRScanResult
from .utils import decode_qr
from .ml_logic import analyse_qr


# ---------------- SIGNUP ---------------- #
class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = UserCreationForm.Meta.model
        fields = ("username", "email", "password1", "password2")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = SignupForm()
    return render(request, "registration/signup.html", {"form": form})


# ---------------- DASHBOARD ---------------- #
@login_required
def dashboard(request):
    total = QRScanResult.objects.filter(user=request.user).count()
    by_risk = QRScanResult.objects.filter(user=request.user).values("risk_level").annotate(c=Count("id"))
    stats = {x["risk_level"]: x["c"] for x in by_risk}

    return render(request, "qr_detector/dashboard.html", {
        "total": total,
        "safe": stats.get(QRScanResult.RISK_SAFE, 0),
        "scam": stats.get(QRScanResult.RISK_SCAM, 0),
        "susp": stats.get(QRScanResult.RISK_SUSPICIOUS, 0),
    })




# ---------------- FILE UPLOAD SCAN ---------------- #
@login_required
def index(request):
    if request.method == "POST":
        form = QRUploadForm(request.POST, request.FILES)
        if form.is_valid():
            img = form.cleaned_data["image"]
            saved_path = default_storage.save(f"qr_uploads/{img.name}", img)
            full_path = default_storage.path(saved_path)

            decoded_text = decode_qr(full_path)
            analysis = analyse_qr(decoded_text or "")

            scan = QRScanResult.objects.create(
                uploaded_image=saved_path,
                decoded_text=decoded_text or "",
                upi_id=analysis["upi_id"],
                name=analysis["name"],
                receiver=analysis["receiver"],
                risk_level=analysis["risk_level"],
                reason=analysis["reason"],
                ml_score=analysis["ml_score"],
                user=request.user
            )
            return redirect("scan_result", scan_id=scan.id)
        else:
            messages.error(request, "Please upload a valid QR image.")
    else:
        form = QRUploadForm()

    return render(request, "qr_detector/index.html", {"form": form})


# ---------------- SCAN RESULT ---------------- #
@login_required
def scan_result(request, scan_id):
    scan = get_object_or_404(QRScanResult, id=scan_id, user=request.user)
    return render(request, "qr_detector/result.html", {"scan": scan})


# ---------------- HISTORY ---------------- #
@login_required
def history(request):
    scans = QRScanResult.objects.filter(user=request.user).order_by("-created_at")[:100]
    return render(request, "qr_detector/history.html", {"scans": scans})


# ---------------- WEBCAM SCAN ---------------- #
@login_required


def webcam_scan(request):
    """
    Handles QR scans from Html5Qrcode (webcam).
    JS sends qr_data via POST (AJAX).
    """
    if request.method == "POST":
        qr_text = request.POST.get("qr_data")

        if not qr_text:
            return JsonResponse({
                "status": "error",
                "message": "No QR data received"
            }, status=400)

        analysis = analyse_qr(qr_text)

        scan = QRScanResult.objects.create(
            decoded_text=qr_text,
            upi_id=analysis.get("upi_id"),
            name=analysis.get("name"),
            receiver=analysis.get("receiver"),
            risk_level=analysis.get("risk_level"),
            reason=analysis.get("reason"),
            ml_score=analysis.get("ml_score"),
            user=request.user
        )

        return JsonResponse({
            "status": "success",
            "scan_id": scan.id,
            "redirect_url": f"/result/{scan.id}/"
        })

    # GET → load webcam page
    return render(request, "qr_detector/webcam.html")









