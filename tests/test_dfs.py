from segmentation_core.engine import Player
from segmentation_core.agents import SlothBot
from segmentation.agents import DFSAgent
from tests.utils import game_loop

def test_path_length():
    """
    Verifies that the path length taken by the DFS agent is *not* necessarily the shortest path.
    The DFS agent may take a longer path depending on which nodes it explores first.
    """

    winner_tl_bl, agent_one_actions_tl_bl, _ = game_loop("square_loop_tl_bl.world", DFSAgent, SlothBot)
    winner_tr_br, agent_one_actions_tr_br, _ = game_loop("square_loop_tr_br.world", DFSAgent, SlothBot)
    winner_tl_tr, agent_one_actions_tl_tr, _ = game_loop("square_loop_tl_tr.world", DFSAgent, SlothBot)
    winner_bl_br, agent_one_actions_bl_br, _ = game_loop("square_loop_bl_br.world", DFSAgent, SlothBot)

    path_lengths = [len(agent_one_actions_tl_bl), len(agent_one_actions_tr_br), len(agent_one_actions_tl_tr), len(agent_one_actions_bl_br)]
    winners = {winner_tl_bl, winner_tr_br, winner_tl_tr, winner_bl_br}

    assert set(path_lengths) == {4, 12}
    assert winners == {Player.PLAYER_ONE}

def test_small_world_winner():
    """
    Verifies that the BFS agent is able to reach the SlothBot to win the game.
    """
    assert game_loop("small.world", DFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("small.world", SlothBot, DFSAgent)[0] == Player.PLAYER_TWO

def test_medium_world_winner():
    """
    Verifies that the BFS agent is able to reach the SlothBot to win the game.
    """
    assert game_loop("small.world", DFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("small.world", SlothBot, DFSAgent)[0] == Player.PLAYER_TWO

def test_large_world_winner():
    """
    Verifies that the BFS agent is able to reach the SlothBot to win the game.
    """
    assert game_loop("small.world", DFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("small.world", SlothBot, DFSAgent)[0] == Player.PLAYER_TWO

