from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# === Hardcoded Discord Webhook URL ===
DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1467553434541625558/fKl1f66ykkbYUxlzxhR-ODuDaskO6bZvEi_Xb7zxeR0MNelnYg3LJBs-ZFCmA2QYDmbK"

@app.route('/api/contact', methods=['POST'])
def contact():
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    message = data.get('message', 'No message provided')

    if not name or not email or not phone:
        return jsonify({"error": "Missing required fields"}), 400

    # Create Discord embed
    embed = {
        "title": "New Client Received",
        "color": 3447003,
        "fields": [
            {"name": "Name", "value": name, "inline": True},
            {"name": "Email", "value": email, "inline": True},
            {"name": "Phone", "value": phone, "inline": True},
            {"name": "Message", "value": message}
        ]
    }

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json={"embeds": [embed]})
        response.raise_for_status()
        return jsonify({"success": True})
    except Exception as e:
        print("Error sending to Discord:", e)
        return jsonify({"error": "Failed to send message"}), 500

if __name__ == "__main__":
    app.run(debug=True)
