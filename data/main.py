from states import state, splash, game_over, mission_complete_state
from states.game import game
from states.menu import menu_state

def main():
    gameCtrl = state.StateManager()
    state_dict = {
        "Splash": splash.SplashState(),
        "MainMenu": menu_state.MainMenuState(),
    	"Game": game.GameState(),
    	"GameOver": game_over.GameOverState(),
    	"MissionComplete": mission_complete_state.MissionCompleteState()
    }
    gameCtrl.setup_states(state_dict, "Splash")
    gameCtrl.main_loop()