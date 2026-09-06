
from segmentation_core.agents import AgentProtocol
from segmentation_core.engine import Action, GameState, Player


def game_loop(
    filename: str,
    agent_one_class: type[AgentProtocol],
    agent_two_class: type[AgentProtocol],
    max_iterations: int | None = None
) -> tuple[Player, list[Action], list[Action]]:
    """
    Helper function to run a game loop between two agents in a given world.

    Parameters:
       `filename`: Path to the world file to load.
       `agent_one_class`: Agent class of player one.
       `agent_two_class`: Agent class of player two.

    Returns:
       The winning player and the list of actions taken by both players.
    """
    agent_one = agent_one_class(Player.PLAYER_ONE)
    agent_one_actions = []
    agent_two = agent_two_class(Player.PLAYER_TWO)
    agent_two_actions = []
    game_state = GameState(filename, max_iterations)

    while not game_state.winner:
        match game_state.active_player:
            case Player.PLAYER_ONE:
                active_agent = agent_one
                active_agent_actions = agent_one_actions
            case Player.PLAYER_TWO:
                active_agent = agent_two
                active_agent_actions = agent_two_actions
            case _:
                raise ValueError("Invalid active player")

        action = active_agent.get_action(game_state)
        active_agent_actions.append(action)
        game_state = game_state.transition(action)

    return game_state.winner, agent_one_actions, agent_two_actions
