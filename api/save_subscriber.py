import os
import json
from http.server import BaseHTTPRequestHandler
import requests

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            name = data.get("name")
            email = data.get("email")

            if not name or not email:
                self.respond(400, {"success": False, "message": "Missing name or email"})
                return

            # DIRECT REST API CALL
            resp = requests.post(
                f"{SUPABASE_URL}/rest/v1/subscribers",
                headers={
                    "apikey": SUPABASE_KEY,
                    "Authorization": f"Bearer {SUPABASE_KEY}",
                    "Content-Type": "application/json",
                    "Prefer": "return=representation",
                },
                json={
                    "name": name,
                    "email": email
                }
            )

            if resp.status_code >= 300:
                self.respond(500, {"success": False, "message": resp.text})
            else:
                self.respond(200, {"success": True})

        except Exception as e:
            self.respond(500, {"success": False, "message": str(e)})

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def respond(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode())
