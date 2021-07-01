from flask import Flask
from flask_cors import CORS

from kube import get_available_game_servers_ordered

app = Flask(__name__)
CORS(app)

@app.route("/alive", methods=['GET'])
def get_alive():
		return {"status": "ok"}

@app.route("/", methods=['GET'])
def get_gameserver():
		servers = get_available_game_servers_ordered()
		if servers and len(servers) > 0:
			return {"status": "ok", "server": servers[0]}
		else:
			return {"status": "ok", "server": None}

if __name__ == "__main__":
	app.run(host="0.0.0.0", port=5000)
