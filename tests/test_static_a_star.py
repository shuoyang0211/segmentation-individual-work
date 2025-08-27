from segmentation_core.engine import Player
from segmentation_core.agents import SlothBot
from segmentation.agents import StaticAStarAgent
from tests.utils import game_loop


def test_path_length():
    """
    Verifies that the path taken by the BFS agent is the shortest path from the
    agent's starting position to the SlothBot's starting position.
    """

    winner_tl_bl, actions_tl_bl, _ = game_loop(
        "worlds/square_loop_tl_bl.world", StaticAStarAgent, SlothBot
    )
    winner_tr_br, actions_tr_br, _ = game_loop(
        "worlds/square_loop_tr_br.world", StaticAStarAgent, SlothBot
    )
    winner_tl_tr, actions_tl_tr, _ = game_loop(
        "worlds/square_loop_tl_tr.world", StaticAStarAgent, SlothBot
    )
    winner_bl_br, actions_bl_br, _ = game_loop(
        "worlds/square_loop_bl_br.world", StaticAStarAgent, SlothBot
    )

    path_lengths = {
        len(actions_tl_bl),
        len(actions_tr_br),
        len(actions_tl_tr),
        len(actions_bl_br),
    }
    winners = {winner_tl_bl, winner_tr_br, winner_tl_tr, winner_bl_br}

    assert set(path_lengths) == {10}
    assert winners == {Player.PLAYER_ONE}


def test_small_world_winner():
    """
    Verifies that the BFS agent is able to reach the SlothBot to win the game.
    """
    assert game_loop("worlds/small.world", StaticAStarAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SlothBot, StaticAStarAgent)[0] == Player.PLAYER_TWO


def test_medium_world_winner():
    """
    Verifies that the BFS agent is able to reach the SlothBot to win the game.
    """
    assert game_loop("worlds/small.world", StaticAStarAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SlothBot, StaticAStarAgent)[0] == Player.PLAYER_TWO


def test_large_world_winner():
    """
    Verifies that the BFS agent is able to reach the SlothBot to win the game.
    """
    assert game_loop("worlds/small.world", StaticAStarAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SlothBot, StaticAStarAgent)[0] == Player.PLAYER_TWO
