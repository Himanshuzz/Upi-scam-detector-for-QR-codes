from django.db import models

class QRScanResult(models.Model):
    RISK_SAFE = "SAFE"
    RISK_SCAM = "SCAM"
    RISK_SUSPICIOUS = "SUSPICIOUS"

    RISK_CHOICES = [
        (RISK_SAFE, "Safe"),
        (RISK_SCAM, "Scam"),
        (RISK_SUSPICIOUS, "Suspicious"),
    ]

    uploaded_image = models.ImageField(upload_to="qr_uploads/")
    decoded_text = models.TextField(blank=True)
    upi_id = models.CharField(max_length=120, blank=True)
    name = models.CharField(max_length=200, blank=True)
    receiver = models.CharField(max_length=200, blank=True)
    risk_level = models.CharField(max_length=20, choices=RISK_CHOICES, default=RISK_SUSPICIOUS)
    reason = models.TextField(blank=True)
    ml_score = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "auth.User",
        on_delete=models.CASCADE,
        related_name="qr_scans",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.upi_id or 'Unknown'} ({self.risk_level})"
