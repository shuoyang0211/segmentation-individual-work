from segmentation_core.agents import SlothBot
from segmentation_core.engine import Player

from segmentation.agents import BFSAgent
from tests.utils import game_loop


def test_basic_worlds():
    """
    Verifies that the BFS agent is able to reach SlothBot to win the game.
    """

    assert game_loop("worlds/small.world", BFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SlothBot, BFSAgent)[0] == Player.PLAYER_TWO

    assert game_loop("worlds/medium.world", BFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/medium.world", SlothBot, BFSAgent)[0] == Player.PLAYER_TWO

    assert game_loop("worlds/large.world", BFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/large.world", SlothBot, BFSAgent)[0] == Player.PLAYER_TWO


def test_path_worlds():
    """
    Verifies that the BFS agent takes an optimal path to SlothBot's starting position.
    """

    winner_dead_end, p1_acts_dead_end, _ = game_loop(
        "worlds/paths/dead_end.world", BFSAgent, SlothBot
    )
    winner_detour, p1_acts_detour, _ = game_loop(
        "worlds/paths/detour.world", BFSAgent, SlothBot
    )
    winner_jail, p1_acts_jail, _ = game_loop(
        "worlds/paths/jail.world", BFSAgent, SlothBot
    )
    winner_labrynth, p1_acts_labrynth, _ = game_loop(
        "worlds/paths/labrynth.world", BFSAgent, SlothBot
    )
    winner_square_loop, p1_acts_square_loop, _ = game_loop(
        "worlds/paths/square_loop.world", BFSAgent, SlothBot
    )
    winner_vortex, p1_acts_vortex, _ = game_loop(
        "worlds/paths/vortex.world", BFSAgent, SlothBot
    )

    assert winner_dead_end == Player.PLAYER_ONE and len(p1_acts_dead_end) == 63
    assert winner_detour == Player.PLAYER_ONE and len(p1_acts_detour) == 42
    assert winner_jail == Player.PLAYER_ONE and len(p1_acts_jail) == 38
    assert winner_labrynth == Player.PLAYER_ONE and len(p1_acts_labrynth) == 48
    assert winner_square_loop == Player.PLAYER_ONE and len(p1_acts_square_loop) == 20
    assert winner_vortex == Player.PLAYER_ONE and len(p1_acts_vortex) == 70
