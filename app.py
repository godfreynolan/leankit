from flask import Flask, request, jsonify
import requests
import config

app = Flask(__name__)

# Config variables from config.py
HOST = config.HOST
BOARD_ID = config.BOARD_ID
LANE_ID = config.LANE_ID
API_TOKEN = config.PLANVIEW_API_TOKEN

@app.route('/create_card', methods=['POST'])
def create_card():
    data = request.get_json()

    # Expecting a 'title' in the JSON payload
    title = data.get('title', 'Untitled Card')

    url = f"https://{HOST}.leankit.com/io/card"
    payload = {
        "destination": {"boardId": f"{BOARD_ID}", "laneId": f"{LANE_ID}"},
        "title": title
    }
    headers = {
        "Authorization": f"Bearer {API_TOKEN}",
        "Accept": "application/json"
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code in (200, 201):
        return jsonify({
            "message": "Card created successfully",
            "card": response.json()
        }), 201
    else:
        return jsonify({
            "message": f"Failed to create card: HTTP {response.status_code}",
            "error": response.text
        }), response.status_code

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
