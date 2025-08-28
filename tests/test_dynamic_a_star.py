from segmentation_core.engine import Player
from segmentation_core.agents import SnakeBot
from segmentation.agents import DynamicAStarAgent
from tests.utils import game_loop

def test_small_world_winner():
    """`
    Verifies that the BFS agent is able to reach the SnakeBot to win the game.
    """
    assert game_loop("worlds/small.world", DynamicAStarAgent, SnakeBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SnakeBot, DynamicAStarAgent)[0] == Player.PLAYER_TWO

def test_medium_world_winner():
    """
    Verifies that the BFS agent is able to reach the SnakeBot to win the game.
    """
    assert game_loop("worlds/small.world", DynamicAStarAgent, SnakeBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SnakeBot, DynamicAStarAgent)[0] == Player.PLAYER_TWO

def test_large_world_winner():
    """
    Verifies that the BFS agent is able to reach the SnakeBot to win the game.
    """
    assert game_loop("worlds/small.world", DynamicAStarAgent, SnakeBot)[0] == Player.PLAYER_ONE
    assert game_loop("worlds/small.world", SnakeBot, DynamicAStarAgent)[0] == Player.PLAYER_TWO