from datetime import MINYEAR
from flask import Flask, render_template, Response, request, jsonify
from master import Game

ENABLE_MULTI = False
games = {}
app = Flask(__name__)

def get_game(gameid):
    if not gameid in games.keys():
        games[gameid] = Game()
    return games[gameid]

@app.route('/')
def main():
    return render_template('../frontend/index.html')


@app.route("/connect", methods=["POST"])
def on_connect():
    game = get_game(int(request.json.get("gameid")))
    return jsonify(game.on_game_entry())


@app.route("/await_start", methods=["GET"])
def await_start():
    game = get_game(int(request.json.get("gameid")))
    def waitforstart():
        while True:
            game.await_game_start()
            yield "data: start\n\n"

    return Response(waitforstart(), mimetype="text/event-stream")


@app.route("/get_cards", methods=["GET"])
def get_bombs():
    game = get_game(int(request.json.get("gameid")))
    return jsonify(game.get_cards())


@app.route("/place_starting_board", methods=["POST"])
def place_starting_board():
    game = get_game(int(request.json.get("gameid")))
    player = request.json.get("player")
    factories = request.json.get("factories")
    silos = request.json.get("silos")
    return jsonify(game.place_starting_board(player, factories, silos))


@app.route("/await_turn", methods=["GET"])
def await_turn():
    game = get_game(int(request.json.get("gameid")))
    def waitforturn():
        while True:
            playercode = game.await_turn_change()
            yield "data: " + '{"player": ' + str(playercode) + "}\n\n"
    return Response(waitforturn(), mimetype="text/event-stream")


@app.route("/get_game_state", methods=["POST"])
def get_game_state():
    game = get_game(int(request.json.get("gameid")))
    player = request.json.get("player")
    return jsonify(game.get_game_state(int(player)))


@app.route("/get_hand_options", methods=["POST"])
def get_hand_options():
    game = get_game(int(request.json.get("gameid")))
    player = request.json.get("player")
    options = game.get_hand_options(player)
    return jsonify(options)


@app.route("/choose_card", methods=["POST"])
def choose_card():
    game = get_game(int(request.json.get("gameid")))
    player = request.json.get("player")
    cardid = request.json.get("cardId")
    valid = game.choose_card(player, cardid)
    return jsonify({"outcome": valid})


@app.route("/place_bomb", methods=["POST"])
def place_bomb():
    game = get_game(int(request.json.get("gameid")))
    player = int(request.json.get("player"))
    coords = request.json.get("coords") # 2 length list
    bombid = request.json.get("bombId")
    success = game.deploy_bomb(player, coords, bombid)
    return jsonify({"outcome": success})

@app.route("/on_disconnect", methods=["POST"])
def on_disconnect():
    if int(request.json.get("gameid")) in games.keys():
        del games[int(request.json.get("gameid"))]
    




if __name__ == '__main__':
    app.debug = True
    app.run(threaded=True, host="0.0.0.0", port=5000)