from states import state, splash
from states.game import game

def main():
    gameCtrl = state.StateManager()
    state_dict = {
        "splash": splash.SplashState(),
    	"Game": game.GameState()
    }
    gameCtrl.setup_states(state_dict, "splash")
    gameCtrl.main_loop()