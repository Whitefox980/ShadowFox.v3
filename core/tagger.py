def get_tags(tool_name, output=""):
    tool = tool_name.lower()
    tags = []

    if "sql" in tool or "sqli" in tool:
        tags += ["injection", "database"]
    if "xss" in tool:
        tags += ["xss", "client-side"]
    if "cmd" in tool or "rce" in tool:
        tags += ["rce", "command"]
    if "lfi" in tool or "rfi" in tool:
        tags += ["file-inclusion"]
    if "ssrf" in tool:
        tags += ["ssrf", "server-side"]
    if "subdomain" in tool:
        tags += ["recon", "enum"]
    if "idor" in tool:
        tags += ["authorization", "object-access"]

    # Dodatni tagovi na osnovu sadržaja
    if "root:x" in output:
        tags.append("passwd-leak")
    if "alert(" in output or "<script>" in output:
        tags.append("script-execution")
    if "200 OK" in output and "admin" in output:
        tags.append("admin-access")

    return list(set(tags))  # bez duplikata
