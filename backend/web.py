from datetime import MINYEAR
from flask import Flask, Response, json, request, jsonify, send_from_directory
from master import Game
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
game = Game()


@app.route("/connect", methods=["POST"])
def on_connect():
    return jsonify(game.on_game_entry())


@app.route("/await_start", methods=["GET"])
def await_start():
    def waitforstart():
        while True:
            game.await_game_start()
            yield "data: start\n\n"

    return Response(waitforstart(), mimetype="text/event-stream")


@app.route("/get_cards", methods=["GET"])
def get_bombs():
    return jsonify(game.get_cards())


@app.route("/place_starting_board", methods=["POST"])
def place_starting_board():
    player = request.json.get("player")
    factories = request.json.get("factories")
    silos = request.json.get("silos")
    return jsonify(game.place_starting_board(player, factories, silos))


@app.route("/await_turn", methods=["GET"])
def await_turn():
    def waitforturn():
        while True:
            playercode = game.await_turn_change()
            yield "data: " + '{"player": ' + str(int(playercode)) + "}\n\n"

    return Response(waitforturn(), mimetype="text/event-stream")


@app.route("/get_game_state", methods=["POST"])
def get_game_state():
    player = request.json.get("player")
    return jsonify(game.get_game_state(int(player)))


@app.route("/get_hand_options", methods=["POST"])
def get_hand_options():
    player = request.json.get("player")
    options = game.get_hand_options(player)
    return jsonify(options)


@app.route("/choose_card", methods=["POST"])
def choose_card():
    player = request.json.get("player")
    cardid = request.json.get("cardId")
    valid = game.choose_card(player, cardid)
    return jsonify({"outcome": valid})


@app.route("/place_bomb", methods=["POST"])
def place_bomb():
    player = int(request.json.get("player"))
    coords = request.json.get("coords")  # 2 length list
    bomb_id = request.json.get("bombId")
    extra = request.json.get("extra")
    success = game.deploy_bomb(player, coords, bomb_id, extra)
    return jsonify({"outcome": success})


@app.route("/skip_turn", methods=["POST"])
def skip_turn():
    player = int(request.json.get("player"))
    success = game.skip_turn(player)
    return jsonify({"outcome": success})


@app.route("/")
@app.route("/<path:static>")
def main(static=None):
    if static is None:
        static = "index.html"
    return send_from_directory("../frontend", static)


if __name__ == "__main__":
    app.debug = True
    app.run(threaded=True, host="0.0.0.0", port=5000)
