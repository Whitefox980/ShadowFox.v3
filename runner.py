import os
import sys
from core.executor import run_all, run_fuzz_modules, run_payload_generator

def banner():
    os.system("clear")
    print("""
███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██╗    ██╗ ██████╗ ███████╗
██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██║    ██║██╔═══██╗██╔════╝
███████╗███████║███████║██████╔╝██║   ██║██║ █╗ ██║██║   ██║█████╗  
╚════██║██╔══██║██╔══██║██╔═══╝ ██║   ██║██║███╗██║██║   ██║██╔══╝  
███████║██║  ██║██║  ██║██║     ╚██████╔╝╚███╔███╔╝╚██████╔╝███████╗
╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝      ╚═════╝  ╚══╝╚══╝  ╚═════╝ ╚══════╝
                         ShadowFox v3 - Offensive Security Toolkit
    """)

def meni():
    print("\n[ MENI ]")
    print("[1] Pokreni sve testove za sve mete")
    print("[2] ShadowFuzz AI (svi fuzz moduli)")
    print("[3] ShadowPayload Generator (AI generisani payloadi)")
    print("[4] Shadow Radar (vizualizacija detekcija)")
    print("[5] White Shadow Advisor (AI zaštitni savetnik)")
    print("[6] Black Shadow Advisor (AI ofanzivni strateg)")
    print("[7] Shadow Operator (centralna kontrola i nadzor)")
    print("[8] Generiši PDF izveštaj")
    print("[0] Izlaz")

def pokreni():
    while True:
        banner()
        meni()
        izbor = input("\n>>> Unesi broj opcije: ").strip()

        if izbor == "1":
            run_all()
        elif izbor == "2":
            run_fuzz_modules()
        elif izbor == "3":
            run_payload_generator()
        elif izbor == "4":
            from core.shadow_radar import run_radar
            run_radar()
        elif izbor == "5":
            from core.white_shadow_advisor import run_white_advisor
            run_white_advisor()
        elif izbor == "6":
            from core.black_shadow_advisor import run_black_advisor
            run_black_advisor()
        elif izbor == "7":
            from core.shadow_operator import run_operator
            run_operator()
        elif izbor == "8":
            from core.shadow_pdf_export import export_pdf_report
            export_pdf_report()
        elif izbor == "0":
            print("[-] Izlazim.")
            sys.exit()
        else:
            input("[!] Nevažeći izbor. Pritisni Enter za nastavak...")

if __name__ == "__main__":
    pokreni()
