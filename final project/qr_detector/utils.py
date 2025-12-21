import cv2

def decode_qr(image_path: str) -> str | None:
    img = cv2.imread(image_path)
    if img is None:
        return None

    detector = cv2.QRCodeDetector()
    data, points, _ = detector.detectAndDecode(img)

    if points is not None and data:
        return data.strip()

    return None
