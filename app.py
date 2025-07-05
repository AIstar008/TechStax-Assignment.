from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["webhook_db"]
collection = db["events"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/webhook', methods=['POST'])
def webhook():
    payload = request.json
    event = request.headers.get('X-GitHub-Event')

    data = {
        "timestamp": datetime.utcnow()
    }

    if event == "push":
        data["action"] = "push"
        data["author"] = payload["pusher"]["name"]
        data["to_branch"] = payload["ref"].split("/")[-1]

    elif event == "pull_request":
        data["action"] = "pull_request"
        pr = payload["pull_request"]
        data["author"] = pr["user"]["login"]
        data["from_branch"] = pr["head"]["ref"]
        data["to_branch"] = pr["base"]["ref"]

    elif event == "merge":
        data["action"] = "merge"
        # Add logic for merge detection if you attempt this (bonus)

    else:
        return jsonify({"message": "Unhandled event"}), 400

    collection.insert_one(data)
    return jsonify({"message": "Event stored"}), 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find().sort("timestamp", -1).limit(10))
    for e in events:
        e["_id"] = str(e["_id"])
        e["timestamp"] = e["timestamp"].strftime("%d %b %Y - %I:%M %p UTC")
    return jsonify(events)

if __name__ == '__main__':
    app.run(debug=True)