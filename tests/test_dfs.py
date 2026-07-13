from segmentation_core.engine import Player
from segmentation_core.agents import SlothBot
from segmentation.agents import DFSAgent
from tests.utils import game_loop


def test_basic_worlds():
    """
    Verifies that the DFS agent is able to reach SlothBot to win the game.
    """

    assert game_loop("worlds/small.world", DFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SlothBot, DFSAgent)[0] == Player.PLAYER_TWO

    assert game_loop("worlds/medium.world", DFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/medium.world", SlothBot, DFSAgent)[0] == Player.PLAYER_TWO

    assert game_loop("worlds/large.world", DFSAgent, SlothBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/large.world", SlothBot, DFSAgent)[0] == Player.PLAYER_TWO


def test_path_length():
    """
    Verifies that the DFS agent takes a valid (according to DFS) path to SlothBot's starting position.
    """

    winner_dead_end, p1_acts_dead_end, _ = game_loop(
        "worlds/path_tests/dead_end.world", DFSAgent, SlothBot
    )
    winner_detour, p1_acts_detour, _ = game_loop(
        "worlds/path_tests/detour.world", DFSAgent, SlothBot
    )
    winner_jail, _, _ = game_loop(
        "worlds/path_tests/jail.world", DFSAgent, SlothBot
    )
    winner_labrynth, _, _ = game_loop(
        "worlds/path_tests/labrynth.world", DFSAgent, SlothBot
    )
    winner_square_loop, p1_acts_square_loop, _ = game_loop(
        "worlds/path_tests/square_loop.world", DFSAgent, SlothBot
    )
    winner_vortex, p1_acts_vortex, _ = game_loop(
        "worlds/path_tests/vortex.world", DFSAgent, SlothBot
    )

    assert winner_dead_end == Player.PLAYER_ONE and len(p1_acts_dead_end) == 63
    assert winner_detour == Player.PLAYER_ONE and len(p1_acts_detour) in [42, 178, 182, 186, 390]
    assert winner_jail == Player.PLAYER_ONE
    assert winner_labrynth == Player.PLAYER_ONE
    assert winner_square_loop == Player.PLAYER_ONE and len(p1_acts_square_loop) == 20
    assert winner_vortex == Player.PLAYER_ONE and len(p1_acts_vortex) in [70, 72, 578, 682, 684, 686]
