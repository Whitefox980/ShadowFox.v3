import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from core.shadow_agent_x import agent_x
import time

def auto_map_and_attack(base_url):
    print(f"\n[+] Povezujem izviđača i AgentX za: {base_url}")
    try:
        r = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[x] Ne mogu da dohvatim: {e}")
        return

    links = [a["href"] for a in soup.find_all("a", href=True)]
    full_urls = [urljoin(base_url, l) for l in links if not l.startswith("javascript")]
    route_set = set(urlparse(l).path for l in full_urls if base_url in l)

    print(f"[i] Pronađeno ruta: {len(route_set)} — selektujem 3 prioriteta...")

    for i, path in enumerate(list(route_set)[:3]):
        target = urljoin(base_url, path)
        print(f"\n[{i+1}] Aktiviram AgentX na: {target}")
        try:
            agent_x(target)
            time.sleep(1)
        except Exception as e:
            print(f"[!] Greška tokom napada na {target}: {e}")
