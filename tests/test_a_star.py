from segmentation_core.engine import Player
from segmentation_core.agents import SlothBot
from segmentation.agents import AStarAgent
from tests.utils import game_loop


def test_path_length():
    """
    Verifies that the path taken by the A* agent is the shortest path from the
    agent's starting position to the SlothBot's starting position.
    """

    winner_tl_bl, actions_tl_bl, _ = game_loop(
        "worlds/square_loop_tl_bl.world", AStarAgent, SlothBot
    )
    winner_tr_br, actions_tr_br, _ = game_loop(
        "worlds/square_loop_tr_br.world", AStarAgent, SlothBot
    )
    winner_tl_tr, actions_tl_tr, _ = game_loop(
        "worlds/square_loop_tl_tr.world", AStarAgent, SlothBot
    )
    winner_bl_br, actions_bl_br, _ = game_loop(
        "worlds/square_loop_bl_br.world", AStarAgent, SlothBot
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
    Verifies that the A* agent is able to reach the SlothBot to win the game.
    """
    assert (
        game_loop("worlds/small.world", AStarAgent, SlothBot)[0]
        == Player.PLAYER_ONE
    )
    assert (
        game_loop("worlds/small.world", SlothBot, AStarAgent)[0]
        == Player.PLAYER_TWO
    )


def test_medium_world_winner():
    """
    Verifies that the A* agent is able to reach the SlothBot to win the game.
    """
    assert (
        game_loop("worlds/medium.world", AStarAgent, SlothBot)[0]
        == Player.PLAYER_ONE
    )
    assert (
        game_loop("worlds/medium.world", SlothBot, AStarAgent)[0]
        == Player.PLAYER_TWO
    )


def test_large_world_winner():
    """
    Verifies that the A* agent is able to reach the SlothBot to win the game.
    """
    assert (
        game_loop("worlds/large.world", AStarAgent, SlothBot)[0]
        == Player.PLAYER_ONE
    )
    assert (
        game_loop("worlds/large.world", SlothBot, AStarAgent)[0]
        == Player.PLAYER_TWO
    )
