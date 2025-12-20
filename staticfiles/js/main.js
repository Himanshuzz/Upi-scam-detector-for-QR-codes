console.log("%cUPI QR Scam Detector Loaded", "color:#38bdf8;font-weight:bold;");

const hideElement = (el) => { if(el) el.style.display="none"; };
const scaleElement = (el, scale=1.08, duration=0.4) => { if(el){ el.style.transform=`scale(${scale})`; el.style.transition=`${duration}s`; } };

// Auto-hide alerts
document.querySelectorAll(".message, .alert").forEach(msg => setTimeout(()=>hideElement(msg),4000));

// Highlight scam
const riskBadge = document.querySelector(".risk-badge");
if(riskBadge && riskBadge.textContent.toLowerCase().includes("scam")) scaleElement(riskBadge);

// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", e => {
        e.preventDefault();
        const target = document.querySelector(anchor.getAttribute("href"));
        if(target) target.scrollIntoView({behavior:"smooth"});
    });
});

// File upload preview
const uploadInput = document.querySelector('input[type="file"]');
const previewContainer = document.querySelector("#qr-preview");
if(uploadInput){
    uploadInput.addEventListener("change", function(){
        const file=this.files[0];
        if(file && previewContainer){
            const reader=new FileReader();
            reader.onload=e=>previewContainer.innerHTML=`<img src="${e.target.result}" class="qr-preview-img" alt="QR Preview">`;
            reader.readAsDataURL(file);
        }
    });
}
