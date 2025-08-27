from typing import Type

from segmentation_core.engine import Action, GameState, Player
from segmentation_core.agents import AgentProtocol


def game_loop(filename: str, agent_one_class: Type[AgentProtocol], agent_two_class: Type[AgentProtocol]) -> tuple[Player, list[Action], list[Action]]:
    """
    Helper function to run a game loop between two agents in a given world.

    Parameters:
       - filename: The name of the world file to load.
       - agent_one_class: The class of the first agent (Player One).
       - agent_two_class: The class of the second agent (Player Two).

    Returns:
       - The winning player (Player.PLAYER_ONE or Player.PLAYER_TWO).
       - The list of actions taken by both players during the game.
    """
    agent_one = agent_one_class(Player.PLAYER_ONE)
    agent_one_actions = []
    agent_two = agent_two_class(Player.PLAYER_TWO)
    agent_two_actions = []
    game_state = GameState(filename)

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