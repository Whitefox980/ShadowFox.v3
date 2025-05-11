from flask import Flask, request
from datetime import datetime
import os

app = Flask(__name__)
LOG_PATH = "logs/incoming_hits.log"

@app.route("/", methods=["GET", "POST"])
def index():
    data = {
        "time": datetime.utcnow().isoformat(),
        "method": request.method,
        "headers": dict(request.headers),
        "args": request.args.to_dict(),
        "form": request.form.to_dict(),
        "json": request.get_json(silent=True),
        "remote": request.remote_addr
    }

    log_line = f"\n=== Ping Detected ===\n{data}\n"

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        f.write(log_line)

    print(log_line)
    return "[✓] ShadowFox ping received", 200

if __name__ == "__main__":
    port = int(os.getenv("LISTENER_PORT", 8088))
    print(f"[+] ShadowFox Listener aktivan na portu {port}")
    app.run(host="0.0.0.0", port=port)
