# runner.py

from core import (
    executor, shadow_dashboard,
    shadow_payloads, shadow_tactic_ai, shadow_stats, shadow_sentinel,
    white_shadow_advisor, black_shadow_advisor, shadow_operator, shadow_mapper,
    shadow_arsenal, shadow_radar, shadow_payload_gen, agent_tactician,
    agent_stats, shadow_log_center, shadow_control, ai_tools
)

objasnjenja = {
    "1": "Pokreće sve testove na svim metama",
    "2": "Omogućava izbor konkretnih testova",
    "3": "Prikazuje prethodno skenirane ranjivosti",
    "4": "AI pravi rezime nalaza sa savetima i eksportuje",
    "5": "Prikazuje sve dostupne payload-e sa klasama",
    "6": "AI generiše nove payload-e",
    "7": "Fuzzuje jedan payload na metama",
    "8": "AI bira najbolji alat i payload",
    "9": "Prikazuje koliko je AI uspešan po meti",
    "10": "AI bira strategiju izvođenja napada",
    "11": "Pravi sistemske bezbednosne savete",
    "12": "AI fokusiran na napad i eksploataciju",
    "13": "Poređenje ofanzivnog i defanzivnog AI saveta",
    "14": "Export oba AI saveta u PDF obliku",
    "15": "AI radi reconnaissance i pravi listu meta",
    "16": "Prikazuje graf raspodele težine nalaza",
    "17": "Centralna kontrola svih agenata",
    "18": "Praćenje logova i anomalija",
    "19": "Analizira logove napada sa AI",
    "20": "Saveti za unapređenje zaštite",
    "21": "Pregled i analiza svih logova",
    "22": "Ručni eksport nalaza u PDF",
    "23": "Vizuelni panel statusa testova i agenata",
    "24": "Ručno zadavanje AI promptova",
    "25": "AI automatski vodi sve faze napada",
    "26": "AI testira XSS fuzzy payload-e",
    "27": "AI testira SQL injection fuzzy napade",
    "28": "AI traži SSRF ranjivosti",
    "29": "Kombinovani AI fuzzy napadi",
    "30": "Sažetak prethodnih skeniranja",
    "31": "Ekstrakcija dataset-a za trening AI",
    "32": "AI klasifikuje payload-e po tipu",
    "33": "Pravi PDF mapu ranjivosti",
    "34": "Prikazuje graf payload-eva po metama",
    "35": "Prikazuje izlaz AI agenta vizuelno",
    "36": "Vizuelizacija meta sa podacima",
    "37": "Filtriranje payload-a po klasi",
    "38": "Ponovno izvođenje uspešnih payload-a",
    "39": "Testira sistem protiv AI napada",
    "40": "Otkriva kako sistem odgovara na napade",
    "41": "Postavljanje tunela za skriveni napad",
    "42": "Loguje povratne odgovore sa meta",
    "43": "AI uči iz prethodnih pokušaja",
    "44": "Prikazuje završnu AI strategiju",
    "45": "AI pravi putanju za napad",
    "46": "Glavni komandni centar",
    "47": "Taktika napada bazirana na AI učenju",
    "48": "Izlaz iz ShadowFox sistema"
}


def meni():
    print("\n=== SHADOWFOX - GLAVNI TERMINAL ===")
    for broj, opis in objasnjenja.items():
        print(f"{broj}. {opis}")
    izbor = input("Izbor: ")
    return izbor
    print("1. Pokreni sve testove (FULL SCAN)")
    print("2. Pokreni odabrane testove (po izboru)")
    print("3. Pregled rezultata")
    print("4. Generiši AI izveštaj (Markdown / PDF)")
    print("5. Shadow Arsenal (baza payload-a sa opisima)")
    print("6. AI Payload Generator (napravi novi payload)")
    print("7. AI Payload Test (fuzz testiranje payload-a)")
    print("8. ShadowAgentX (AI bira modul + payload)")
    print("9. ShadowAgentX Statistika (uspešnost napada)")
    print("10. Shadow TacticAI (AI bira taktiku napada)")
    print("11. White Shadow AI (sistemski bezbednosni savetnik)")
    print("12. Black Shadow Advisor (ofanzivni savetnik)")
    print("13. Shadow Control Panel (uporedi oba saveta)")
    print("14. Shadow Strategijski Izveštaj (PDF sa oba saveta)")
    print("15. Shadow Mapper (AI izviđač + lista meta)")
    print("16. ShadowRadar (grafička raspodela SEVERITY)")
    print("17. ShadowOperator (kontrola svih agenata)")
    print("18. Shadow Sentinel (log senzor i AI detekcija)")
    print("19. ShadowAgentX analiza logova")
    print("20. ShadowAgentX preporuke (taktike i poboljšanja)")
    print("21. Shadow Log Center (analiza logova)")
    print("22. Shadow PDF Export (ručni izvoz)")
    print("23. Shadow Dashboard (vizuelni prikaz statusa)")
    print("24. Shadow Manual AI (rucna AI eksploatacija)")
    print("25. Shadow Auto AI (puni automatski AI mod)")
    print("26. Shadow Fuzz XSS (AI fuzzy za XSS)")
    print("27. Shadow Fuzz SQLi (AI fuzzy za SQLi)")
    print("28. Shadow Fuzz SSRF (AI fuzzy za SSRF)")
    print("29. Shadow Fuzz All-in-One (AI fuzzy kombo)")
    print("30. ShadowScan Log Summary")
    print("31. Shadow Dataset Extractor")
    print("32. ShadowAgentX payload klasa i klasifikacija")
    print("33. Shadow Heatmap Generator (PDF)")
    print("34. Shadow Payload Graph")
    print("35. ShadowAgentX Vizuelni Output")
    print("36. ShadowMapper Target Viewer")
    print("37. Shadow Arsenal Filter")
    print("38. Shadow Repeater (ponovi uspešne napade)")
    print("39. Shadow Backfire (AI test protiv nas)")
    print("40. Shadow Reverse Engine (detekcija odbrane)")
    print("41. ShadowTunnel (tunelovanje sa napadom)")
    print("42. Shadow Exploit Sink (log eksternih odgovora)")
    print("43. ShadowAgentX Feedback Loop")
    print("44. Shadow Strategija Output (PDF)")
    print("45. ShadowMapper + Planiranje napada")
    print("46. Shadow Operator Panel")
    print("47. ShadowAgentX Tactician AI")
    print("48. Izlaz")
    return input("\nIzbor: ")

def pokreni():
    while True:
        izbor = meni()
        if izbor == "1":
            executor.run_all()
        elif izbor == "2":
            executor.run_selected()
        elif izbor == "3":
            executor.show_results()
        elif izbor == "4":
            shadow_pdf_export.export_strategic()
        elif izbor == "5":
            shadow_arsenal.launch()
        elif izbor == "6":
            shadow_payload_gen.generate()
        elif izbor == "7":
            shadow_payloads.run_test()
        elif izbor == "8":
            executor.run_all_headless()
        elif izbor == "9":
            agent_stats.analyze()
        elif izbor == "10":
            agent_tactician.recommend()
        elif izbor == "11":
            white_shadow_advisor.advise()
        elif izbor == "12":
            black_shadow_advisor.advise()
        elif izbor == "13":
            shadow_control.compare()
        elif izbor == "14":
            shadow_pdf_export.export_full()
        elif izbor == "15":
            shadow_mapper.map_targets()
        elif izbor == "16":
            shadow_radar.generate()
        elif izbor == "17":
            shadow_operator.launch()
        elif izbor == "18":
            shadow_sentinel.monitor_log()
        elif izbor == "19":
            agent_stats.display_logs()
        elif izbor == "20":
            agent_tactician.improve()
        elif izbor == "21":
            shadow_log_center.analyze()
        elif izbor == "22":
            shadow_pdf_export.export_manual()
        elif izbor == "23":
            shadow_dashboard.show()
        elif izbor == "24":
            shadow_ai_manual.ai_manual()
        elif izbor == "25":
            executor.run_ai_full()
        elif izbor == "26":
            executor.run_fuzz("xss")
        elif izbor == "27":
            executor.run_fuzz("sqli")
        elif izbor == "28":
            executor.run_fuzz("ssrf")
        elif izbor == "29":
            executor.run_all_fuzz()
        elif izbor == "30":
            executor.log_summary()
        elif izbor == "31":
            shadow_pdf_export.extract_dataset()
        elif izbor == "32":
            ai_tools.classify_severity()
        elif izbor == "33":
            shadow_pdf_export.generate_heatmap()
        elif izbor == "34":
            shadow_pdf_export.graph_payloads()
        elif izbor == "35":
            shadow_dashboard.render_viz()
        elif izbor == "36":
            shadow_mapper.view_targets()
        elif izbor == "37":
            shadow_arsenal.filter_by_tags()
        elif izbor == "38":
            executor.repeat_hits()
        elif izbor == "39":
            executor.test_backfire()
        elif izbor == "40":
            executor.reverse_engine()
        elif izbor == "41":
            executor.start_tunnel()
        elif izbor == "42":
            executor.catch_exploit()
        elif izbor == "43":
            agent_stats.feedback_loop()
        elif izbor == "44":
            shadow_pdf_export.export_strategic_report()
        elif izbor == "45":
            shadow_mapper.plan_attacks()
        elif izbor == "46":
            shadow_operator.panel()
        elif izbor == "47":
            agent_tactician.visual_ai()
        elif izbor == "48":
            print("Zatvaranje...")
            break
        else:
            print("Nepoznata komanda.")

if __name__ == "__main__":
    pokreni()
