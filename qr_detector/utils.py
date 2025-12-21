import cv2

def decode_qr(image_path: str) -> str | None:
    """
    Decode QR code using OpenCV (Render-safe).
    """
    img = cv2.imread(image_path)
    if img is None:
        return None

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if points is not None and data:
        return data.strip()

    return None
