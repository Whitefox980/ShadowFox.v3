from core.white_shadow_advisor import generate_defensive_advice
from core.black_shadow_advisor import black_shadow_think

def run_dual_advisors():
    print("\n==================== WHITE SHADOW ADVISOR ====================")
    try:
        generate_defensive_advice()
    except Exception as e:
        print(f"[x] White Advisor Error: {e}")

    print("\n==================== BLACK SHADOW ADVISOR ====================")
    try:
        black_shadow_think()
    except Exception as e:
        print(f"[x] Black Advisor Error: {e}")
