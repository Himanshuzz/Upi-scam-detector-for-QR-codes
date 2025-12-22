/* ================================
   UPI QR Scam Detector – UI Script
================================ */

console.log(
  "%cUPI QR Scam Detector Loaded",
  "color:#38bdf8;font-weight:bold;font-size:14px;"
);

/* ---------- Utility Functions ---------- */

// Hide an element safely
const hideElement = (el) => {
  if (el) el.style.display = "none";
};

// Apply scale animation
const scaleElement = (el, scale = 1.08, duration = 0.4) => {
  if (!el) return;
  el.style.transition = `transform ${duration}s ease`;
  el.style.transform = `scale(${scale})`;
};

/* ---------- Auto-hide Alerts ---------- */

document.querySelectorAll(".message, .alert").forEach((msg) => {
  setTimeout(() => hideElement(msg), 4000);
});

/* ---------- Highlight Scam Result ---------- */

const riskBadge = document.querySelector(".risk-badge");

if (riskBadge) {
  const riskText = riskBadge.textContent.toLowerCase();
  if (riskText.includes("scam") || riskText.includes("high")) {
    scaleElement(riskBadge, 1.12);
  }
}

/* ---------- Smooth Scrolling ---------- */

document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
  anchor.addEventListener("click", (e) => {
    const targetId = anchor.getAttribute("href");
    const targetEl = document.querySelector(targetId);

    if (!targetEl) return;

    e.preventDefault();
    targetEl.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  });
});

/* ---------- QR File Upload Preview ---------- */

const uploadInput = document.querySelector('input[type="file"]');
const previewContainer = document.querySelector("#qr-preview");

if (uploadInput && previewContainer) {
  uploadInput.addEventListener("change", () => {
    const file = uploadInput.files[0];
    if (!file) return;

    // Allow only images
    if (!file.type.startsWith("image/")) {
      previewContainer.innerHTML =
        "<p class='error-text'>Please upload a valid image file</p>";
      return;
    }

    const reader = new FileReader();

    reader.onload = (e) => {
      previewContainer.innerHTML = `
        <img 
          src="${e.target.result}" 
          class="qr-preview-img" 
          alt="QR Code Preview"
        >
      `;
    };

    reader.readAsDataURL(file);
  });
}
