import requests
from core.fuzz_headers import fuzz_headers
from core.fuzz_param_splitter import fuzz_param_split
from core.fuzz_http_methods import fuzz_methods
from core.fuzz_json_body import fuzz_json
from core.agent_logger import log_agent_action

def run_and_log(url, module, payload, reason):
    status = "?"
    reflected = False
    size = 0

    try:
        if module == "headers":
            fuzz_headers(url)
            r = requests.get(url, timeout=5)

        elif module == "params":
            test_url = url.replace("FUZZ", payload)
            fuzz_param_split(test_url)
            r = requests.get(test_url, timeout=5)

        elif module == "methods":
            fuzz_methods(url)
            r = requests.get(url, timeout=5)

        elif module == "json":
            fuzz_json(url)
            r = requests.post(url, json={"test": payload}, timeout=5)

        else:
            print(f"[x] Nepoznat modul: {module}")
            return

        status = r.status_code
        reflected = payload in r.text
        size = len(r.text)

    except Exception as e:
        print(f"[!] Greška tokom testiranja: {e}")

    log_agent_action(
        url=url,
        module=module,
        payload=payload,
        status=status,
        reflected=reflected,
        reason=reason,
        result_size=size
    )
