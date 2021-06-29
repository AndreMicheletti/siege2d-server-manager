import json
from flask import Flask, request

app = Flask(__name__)

FILE = "./data.json"

def get_state() -> dict:
	with open(FILE, "r") as f:
		return json.load(f)

def write_state(new_state: dict):
		with open(FILE, "w") as f:
			json.dump(new_state, fp=f)

@app.route("/", methods=['GET'])
def get_status():
		return get_state()

@app.route("/status", methods=['POST'])
def post_status():
		data = request.json
		state = get_state()
		new_state = {
			**state,
			data["uuid"]: data
		}
		with open(FILE, "w") as f:
			json.dump(new_state, fp=f)
		return {"status": "ok"}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
