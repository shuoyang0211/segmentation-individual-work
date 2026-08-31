from segmentation_core.agents import SnakeBot
from segmentation_core.engine import Player

from segmentation.agents import StudentAgent
from tests.utils import game_loop


def test_small_world_winner():
    """
    Verifies that the student's agent is able to defeat SnakeBot.
    """
    assert game_loop("worlds/small.world", StudentAgent, SnakeBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SnakeBot, StudentAgent)[0] == Player.PLAYER_TWO


def test_medium_world_winner():
    """
    Verifies that the student's agent is able to defeat SnakeBot.
    """
    assert game_loop("worlds/medium.world", StudentAgent, SnakeBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/medium.world", SnakeBot, StudentAgent)[0] == Player.PLAYER_TWO


def test_large_world_winner():
    """
    Verifies that the student's agent is able to defeat SnakeBot.
    """
    assert game_loop("worlds/large.world", StudentAgent, SnakeBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/large.world", SnakeBot, StudentAgent)[0] == Player.PLAYER_TWO
