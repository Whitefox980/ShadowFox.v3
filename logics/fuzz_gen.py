import urllib.parse
import base64

def fuzz_payload(base):
    results = []

    # Original
    results.append(base)

    # URL encode
    results.append(urllib.parse.quote(base))

    # Double URL encode
    results.append(urllib.parse.quote(urllib.parse.quote(base)))

    # Base64
    results.append(base64.b64encode(base.encode()).decode())

    # Hex encoding
    results.append(''.join(['\\x' + hex(ord(c))[2:] for c in base]))

    # HTML entity encoding
    html_entity = ''.join([f'&#{ord(c)};' for c in base])
    results.append(html_entity)

    # Unicode escape
    results.append(base.encode('unicode_escape').decode())

    # Obfuscated injection
    results.append(base.replace("<", "<scr<script>ipt>").replace(">", "</scr<script>ipt>"))

    # Mixed case
    results.append(''.join([c.upper() if i % 2 else c.lower() for i, c in enumerate(base)]))

    return list(set(results))  # bez duplikata
