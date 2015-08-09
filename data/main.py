from state import StateManager
from states import splash, game

def main():
    gameCtrl = StateManager()
    state_dict = {
        "splash": splash.SplashState(),
    	"Game": game.GameState()
    }
    gameCtrl.setup_states(state_dict, "splash")
    gameCtrl.main_loop()