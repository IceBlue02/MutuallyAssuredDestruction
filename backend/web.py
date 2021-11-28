from datetime import MINYEAR
from flask import Flask, json, render_template, Response, request, jsonify
from master import Game

app = Flask(__name__)
game = Game()

@app.route('/')
def main():
    return render_template('../frontend/index.html')

@app.route("/place_bomb", methods=["POST"])
def place_bomb():
    player = int(request.json.get("player"))
    coords = request.json.get("coords") # 2 length list
    bombid = request.json.get("bombid") 
    success = game.deploy_bomb(player, coords, bombid)
    return jsonify({"outcome": success})


@app.route("/get_hand_options", methods=["POST"])
def get_hand_options():
    player = request.form.get("player")
    #options = Game.get_hand_options(player) 
    options = [1, 4, 7, 9] # TEST
    return jsonify(options)

@app.route("/place_starting_board", methods=["POST"])
def place_starting_board():
    player = request.json.get("player")
    factories = request.json.get("factories")
    silos = request.json.get("silos") 
    print(player, factories, silos)

    return jsonify(game.place_starting_board(player, factories, silos))



@app.route("/get_game_state", methods=["POST"])
def get_game_state():
    player = request.json.get("player")
    return jsonify(game.get_game_state(int(player)))
    return False


@app.route("/get_cards", methods=["GET"])
def get_bombs():
    return jsonify(game.get_cards())

@app.route("/connect", methods=["POST"])
def on_connect():
    return jsonify(game.on_game_entry())

@app.route("/await_turn", methods=["GET"])
def await_turn():
    def waitforturn():
        while True:
            playercode = game.await_turn_change()
            yield "data: " + '{"player": ' + str(playercode) + "}\n\n"

    print(waitforturn())
    return Response(waitforturn(), mimetype="text/event-stream")


@app.route("/await_start", methods=["GET"])
def await_start():
    def waitforstart():
        while True:
            game.await_game_start()
            yield "data: start\n\n"

    return Response(waitforstart(), mimetype="text/event-stream")

@app.route("/trigger_turn_change")
def TEST():
    game.trigger_turn_change()
    return "Hell Yeah"


if __name__ == '__main__':
    app.debug = True 
    app.run(threaded=True, host="0.0.0.0", port=5000)