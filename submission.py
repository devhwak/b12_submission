import json
import hmac
import hashlib
import urllib.request
from datetime import datetime, timezone

# === CONFIG ===
SIGNING_SECRET = b"hello-there-from-b12"
URL = "https://b12.io/apply/submission"

payload = {
    "action_run_link": "https://github.com/yourname/yourrepo/actions/runs/123456789",
    "email": "oskar.emil.lindstrom@gmail.com",
    "name": "Oskar Lindström",
    "repository_link": "https://github.com/devhwak/yourrepo",
    "resume_link": "https://pdf-or-html-or-linkedin.example.com",
    "timestamp": datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
}

# Canonical JSON: sorted keys, compact separators, UTF-8
body = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")

# HMAC-SHA256 signature
digest = hmac.new(SIGNING_SECRET, body, hashlib.sha256).hexdigest()
signature = f"sha256={digest}"

req = urllib.request.Request(
    URL,
    data=body,
    headers={
        "Content-Type": "application/json",
        "X-Signature-256": signature,
    },
    method="POST",
)

with urllib.request.urlopen(req) as resp:
    response_body = resp.read().decode("utf-8")
    data = json.loads(response_body)

    if data.get("success"):
        print("Submission receipt:", data["receipt"])
    else:
        raise RuntimeError("Submission failed:", data)
