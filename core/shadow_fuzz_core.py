from core.fuzz_headers import fuzz_headers
from core.fuzz_param_splitter import fuzz_param_split
from core.fuzz_http_methods import fuzz_methods
from core.fuzz_json_body import fuzz_json

def fuzz_menu():
    print("\n[=] ShadowFuzzCore Modul")
    print("1. Header Fuzz          → User-Agent, Referer, X-Forwarded-For...")
    print("2. Param Split Fuzz     → ?x=1&admin=true, #token...")
    print("3. HTTP Method Fuzz     → PUT, DELETE, PATCH...")
    print("4. JSON Body Fuzz       → API fuzz sa isAdmin, debug, root...")
    print("0. Nazad")

def launch_fuzz_core():
    while True:
        fuzz_menu()
        izbor = input("Izaberi Fuzz modul: ").strip()
        
        if izbor == "1":
            url = input("Unesi URL za Header Fuzz: ").strip()
            fuzz_headers(url)

        elif izbor == "2":
            url = input("Unesi URL sa FUZZ za Param Split: ").strip()
            fuzz_param_split(url)

        elif izbor == "3":
            url = input("Unesi URL za HTTP Method Fuzz: ").strip()
            fuzz_methods(url)

        elif izbor == "4":
            url = input("Unesi URL za JSON POST Fuzz: ").strip()
            fuzz_json(url)

        elif izbor == "0":
            break

        else:
            print("[x] Nepoznata opcija.")
