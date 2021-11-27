from backend.master import building, state


class Tile:
    def __init__(self, state, building):
        self.state = state
        self.building = building

    def get_building():
        return building
    
    def get_state():
        return state

    def set_building(building):
        self.building = building

    def set_state(state):
        self.state = state