from datetime import MINYEAR
from flask import Flask, render_template, request, Response, jsonify
import threading
import random


class Game:
    def __init__(self):
        self.turn = 1
        self.bombs = [1, 2, 3, 4, 5, 6, 7, 8]
        self.turnevent = threading.Event()
        self.board = [[1, 0, 0, 2, 0], [0, 1, 3, 0, 0]]
        
    def await_turn_change(self):
        print("waiting")
        self.turnevent.wait()
        print("event given")
        return self.turn

    def __change_turn(self):
        self.turn *= -1
        print(f"turn: {self.turn}")
        self.turnevent.set()
        print(self.turn)
        self.turnevent.clear()

    def get_hand_options(self, player):
        if player == self.turn:
            return random.sample(self.bombs, 3)
        else:
            return False

    def place_bomb(self, player, coord, bombid):
        print(f"{player}, {self.turn}, {coord}, {bombid}")
        print("placed")
        if int(player) == self.turn:
            print("Yes")
            self.__change_turn()    
        else:
            return False

app = Flask(__name__)
game = Game()

@app.route('/')
def main():
    return render_template('../frontend/index.html')

@app.route("/place_bomb", methods=["POST"])
def place_bomb():
    player = request.form.get("player")
    coords = request.form.get("position") # 2 length list
    bombid = request.form.get("bombid") 
    game.place_bomb(player, coords, bombid)
    return jsonify({"status": 1})


@app.route("/get_hand_options", methods=["POST"])
def get_hand_options():
    player = request.form.get("player")
    options = game.get_hand_options(player) 
    return jsonify(options)


@app.route("/get_game_state", methods=["POST"])
def get_game_state():
    return jsonify(game.getState())
    return False

@app.route("/await_turn", methods=["POST"])
def await_turn():
    def waitforturn():
        while True:
            playercode = game.await_turn_change()
            print("YAY")
            yield "event: turn\ndata: " + '{"player": ' + str(playercode) + "}\n\n"

    return Response(waitforturn(), mimetype="text/event-stream")


if __name__ == '__main__':
    app.debug = True 
    app.run(threaded=True, host="0.0.0.0", port=5000)



        


    

