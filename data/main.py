from state import StateManager
from states import splash

def main():
    game = StateManager()
    state_dict = {
        "splash": splash.SplashState()
    }
    game.setup_states(state_dict, "splash")
    game.main_loop()