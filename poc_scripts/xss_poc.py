
from utils.log_utils import classify_severity
# pri vrhu
from logics.log_utils import log_to_sheet

# kad nađe ranjivost
severity = classify_severity("Reflektovani XSS pronađen!")
log_to_sheet("xss_poc.py", "Reflektovani XSS pronađen!") + f' | Severity: {{severity}}')

# kad ne nađe
severity = classify_severity("Nema refleksije")
log_to_sheet("xss_poc.py", "Nema refleksije") + f' | Severity: {{severity}}')
