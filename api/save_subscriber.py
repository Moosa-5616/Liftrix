import os
import json
from supabase import create_client
from http.server import BaseHTTPRequestHandler

# Load Supabase environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            # Read the request body
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length)
            data = json.loads(body)

            name = data.get("name")
            email = data.get("email")

            if not name or not email:
                self.respond(400, {"success": False, "message": "Missing name or email"})
                return

            # Insert into Supabase
            supabase.table("subscribers").insert({
                "name": name,
                "email": email
            }).execute()

            self.respond(200, {"success": True})

        except Exception as e:
            self.respond(500, {"success": False, "message": str(e)})

    def respond(self, status, payload):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
