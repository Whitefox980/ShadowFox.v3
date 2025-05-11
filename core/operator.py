import os
from dotenv import load_dotenv

load_dotenv()
LISTENER_URL = os.getenv("LISTENER_URL", "https://your-default.ngrok.io")
LISTENER_PORT = os.getenv("LISTENER_PORT", "8088")

class Operator:
    def __init__(self):
        self.listener_url = LISTENER_URL
        self.listener_port = LISTENER_PORT
        self.agents = {
            "mapper": "core/target_mapper.py",
            "agentx": "core/shadow_agent_x.py",
            "logger": "core/agent_logger.py",
            "tactician": "core/agent_tactician.py",
            "stats": "core/agent_stats.py",
            "advisor_white": "core/white_shadow_advisor.py",
            "advisor_black": "core/black_shadow_advisor.py",
            "sync": "core/agent_x_auto_sync.py"
        }

    def report(self):
        print("\n[SHADOW OPERATOR] Pregled:")
        print(f"- Listener URL: {self.listener_url}")
        print(f"- Listener Port: {self.listener_port}")
        print("- Aktivni agenti:")
        for k in self.agents:
            print(f"  → {k}")

    def get_listener(self):
        return self.listener_url

    def activate_agent(self, name):
        if name not in self.agents:
            print(f"[x] Nepoznat agent '{name}'")
            return
        print(f"[+] Aktiviram: {name}")
        os.system(f"python3 {self.agents[name]}")

    def update_listener(self, new_url):
        self.listener_url = new_url
        print(f"[✓] Listener URL ažuriran: {self.listener_url}")

    # === SERVISI 1.x ===

    def menu_services(self):
        while True:
            print("\n[1.x] ShadowFox Servisi:")
            print(" 1.1 Pokreni Listener Server")
            print(" 1.2 Startuj Ngrok HTTP tunel")
            print(" 1.3 Pokreni No-IP update")
            print(" 1.4 Prikaži status servisa")
            print(" 0. Nazad")
            izbor = input("> ")

            if izbor == "1.1":
                os.system(f"python3 core/listener_server.py")
            elif izbor == "1.2":
                os.system("ngrok http 8088 &")
            elif izbor == "1.3":
                os.system("noip2 -C && noip2")
            elif izbor == "1.4":
                print(f"\nListener URL: {self.listener_url}")
                print(f"Port: {self.listener_port}")
            elif izbor == "0":
                break
            else:
                print("Nepoznata opcija.")
