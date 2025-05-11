def generate_ui(summary):
    print("\n" + "="*40)
    print("     SHADOW LOG CENTER - REZIME")
    print("="*40)
    for vuln_type, count in summary.items():
        if count > 0:
            print(f" - {vuln_type:<18}: {count}")
    print("="*40 + "\n")
