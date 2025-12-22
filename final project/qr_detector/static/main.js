const RENDER_URL = "https://upi-scam-detector-for-qr-codes-15.onrender.com";

function scanQR() {
  const fileInput = document.getElementById("qrInput");
  const result = document.getElementById("result");

  if (!fileInput.files.length) {
    result.innerText = "Please select a QR image";
    return;
  }

  const formData = new FormData();
  formData.append("image", fileInput.files[0]);

  fetch(`${RENDER_URL}/api/scan/`, {
    method: "POST",
    body: formData
  })
  .then(res => res.json())
  .then(data => {
    result.innerText = data.message || "Scan complete";
  })
  .catch(() => {
    result.innerText = "Server error";
  });
}
