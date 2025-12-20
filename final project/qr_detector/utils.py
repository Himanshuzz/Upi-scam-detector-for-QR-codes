import cv2
from pyzbar.pyzbar import decode as pyzbar_decode
from PIL import Image

def decode_qr(image_path: str) -> str | None:
    """
    First try Pyzbar (very accurate), then fallback to OpenCV QRCodeDetector.
    """
    # --- Pyzbar ---
    try:
        pil_img = Image.open(image_path)
        decoded = pyzbar_decode(pil_img)
        if decoded:
            return decoded[0].data.decode("utf-8").strip()
    except Exception:
        pass

    # --- Fallback OpenCV ---
    img = cv2.imread(image_path)
    if img is None:
        return None

    detector = cv2.QRCodeDetector()
    data, pts, _ = detector.detectAndDecode(img)
    if pts is not None and data:
        return data.strip()
    return None
