def classify_severity(response_text):
    """
    Klasifikuj odgovor servera po ozbiljnosti potencijalne ranjivosti.
    """
    text = response_text.lower()

    high = ["root:x", "sql syntax", "command executed", "unauthorized", "database error"]
    medium = ["warning", "stack trace", "exception", "undefined", "invalid"]
    low = ["not found", "missing", "403 forbidden"]

    for kw in high:
        if kw in text:
            return "HIGH"
    for kw in medium:
        if kw in text:
            return "MEDIUM"
    for kw in low:
        if kw in text:
            return "LOW"

    return "INFO"
