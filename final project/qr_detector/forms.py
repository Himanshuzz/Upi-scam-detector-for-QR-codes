from django import forms

class QRUploadForm(forms.Form):
    image = forms.ImageField(
        label="Upload QR Code Image",
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )
