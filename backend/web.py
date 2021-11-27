from datetime import MINYEAR
from flask import Flask, render_template, Response, jsonify

app = Flask(__name__)
#game = Game()

@app.route('/')
def main():
    return render_template('../frontend/index.html')

@app.route("/place_bomb", methods=["POST"])
def place_bomb():
    player = request.form.get("player")
    coords = request.form.get("position") # 2 length list
    bombid = request.form.get("bombid") 
    #Game.place_bomb(player, coords, bombid)


@app.route("/get_hand_options", methods=["POST"])
def get_hand_options():
    player = request.form.get("player")
    #options = Game.get_hand_options(player) 
    options = [1, 4, 7, 9] # TEST
    return jsonify(options)


@app.route("/get_game_state", methods=["POST"])
def get_game_state():
    #return jsonify(Game.getState())
    return False

@app.route("/await_turn", methods=["POST"])
def await_turn():
    def waitforturn():
        while True:
            #playercode = game.await_turn_change()
            yield "event: turn\ndata: " + '{"player": ' + str(playercode) + "}\n\n"

    return Response(waitforturn(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.debug = True 
    app.run(threaded=True, host="0.0.0.0", port=5000)
