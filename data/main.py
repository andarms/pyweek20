from states import state, splash, game_over
from states.game import game

def main():
    gameCtrl = state.StateManager()
    state_dict = {
        "Splash": splash.SplashState(),
    	"Game": game.GameState(),
    	"GameOver": game_over.GameOverState()
    }
    gameCtrl.setup_states(state_dict, "Splash")
    gameCtrl.main_loop()