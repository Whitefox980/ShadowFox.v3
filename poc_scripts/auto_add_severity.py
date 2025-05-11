def classify_severity(response_text):
    """
    Jednostavna klasifikacija težine ranjivosti na osnovu sadržaja odgovora.
    Možeš proširiti sa AI kasnije.
    """
    response_text = response_text.lower()

    high_indicators = ["root:x", "sql syntax", "admin panel", "command executed", "unauthorized access"]
    medium_indicators = ["error", "undefined", "stack trace", "warning", "unexpected"]
    low_indicators = ["not found", "403 forbidden", "missing", "invalid"]

    for pattern in high_indicators:
        if pattern in response_text:
            return "HIGH"
    for pattern in medium_indicators:
        if pattern in response_text:
            return "MEDIUM"
    for pattern in low_indicators:
        if pattern in response_text:
            return "LOW"
    return "INFO"
