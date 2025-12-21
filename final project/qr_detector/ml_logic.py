import re

UPI_PATTERN = r"[a-zA-Z0-9.\-_]{2,256}@[a-zA-Z]{2,64}"

BLACKLISTED_UPI = [
    "fraud@paytm", "donation@upi", "help@upi", "covidrelief@upi",
    "supportbank@icici", "freegift@ybl", "govtrefund@ybl",
]

SUSPICIOUS_WORDS = [
    "donation", "relief", "support", "gift", "lucky", "reward",
    "win", "refund", "bonus", "help fund", "fund transfer"
]

def analyse_qr(decoded_text: str):
    if not decoded_text:
        return {
            "upi_id": "",
            "name": "",
            "receiver": "",
            "risk_level": "SUSPICIOUS",
            "reason": "QR does not contain valid text",
            "ml_score": 0
        }

    # Extract UPI ID
    upi_match = re.search(UPI_PATTERN, decoded_text)
    upi = upi_match.group(0) if upi_match else ""

    # Name in "pa" or "pn" param
    name = ""
    match_name = re.search(r"pn=([^&]+)", decoded_text)
    if match_name:
        name = match_name.group(1).replace("%20", " ")

    # Receiver
    receiver = name

    # Scam checks
    ml_score = 0
    reason = "Seems safe."

    if upi in BLACKLISTED_UPI:
        ml_score += 90
        reason = "UPI ID is blacklisted."
    else:
        for keyword in SUSPICIOUS_WORDS:
            if keyword.lower() in decoded_text.lower():
                ml_score += 60
                reason = f"Suspicious word detected: {keyword}"
                break

    # Classification
    if ml_score >= 80:
        risk = "SCAM"
    elif ml_score >= 50:
        risk = "SUSPICIOUS"
    else:
        risk = "SAFE"

    return {
        "upi_id": upi,
        "name": name,
        "receiver": receiver,
        "risk_level": risk,
        "reason": reason,
        "ml_score": ml_score,
    }
