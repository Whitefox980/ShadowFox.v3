import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from openai import OpenAI

client = OpenAI()

def map_target_structure(base_url):
    print(f"\n[+] Mapa mete: {base_url}")

    try:
        r = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")
    except Exception as e:
        print(f"[x] Ne mogu da dohvatim: {e}")
        return

    forms = soup.find_all("form")
    links = [a["href"] for a in soup.find_all("a", href=True)]
    inputs = [i.get("name") for i in soup.find_all("input") if i.get("name")]

    all_links = [urljoin(base_url, l) for l in links if not l.startswith("javascript")]
    route_set = set(urlparse(l).path for l in all_links if base_url in l)

    summary = {
        "url": base_url,
        "routes": list(route_set),
        "input_fields": inputs,
        "forms_detected": len(forms),
        "total_links": len(all_links)
    }

    prompt = f"""
Na osnovu strukture ove mete, predloži plan skeniranja i prioritete.

Ulaz:
{summary}

Vrati plan u koracima: gde krenuti, koje module aktivirati, na šta paziti.
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    print("\n[AI IZVIĐAČKI PLAN]:\n")
    print(response.choices[0].message.content.strip())
