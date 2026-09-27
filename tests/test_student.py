from segmentation_core.agents import SnakeBot
from segmentation_core.engine import Player

from segmentation.agents import StudentAgent
from tests.utils import game_loop


# def test_small_world_winner():
#     """
#     Verifies that the student's agent is able to defeat SnakeBot.
#     """
#     assert game_loop("worlds/small.world", StudentAgent, SnakeBot)[0] == Player.PLAYER_ONE
#     assert game_loop("worlds/small.world", SnakeBot, StudentAgent)[0] == Player.PLAYER_TWO


# def test_medium_world_winner():
#     """
#     Verifies that the student's agent is able to defeat SnakeBot.
#     """
#     assert game_loop("worlds/medium.world", StudentAgent, SnakeBot)[0] == Player.PLAYER_ONE
#     assert game_loop("worlds/medium.world", SnakeBot, StudentAgent)[0] == Player.PLAYER_TWO


# def test_large_world_winner():
#     """
#     Verifies that the student's agent is able to defeat SnakeBot.
#     """
#     assert game_loop("worlds/large.world", StudentAgent, SnakeBot)[0] == Player.PLAYER_ONE
#     assert game_loop("worlds/large.world", SnakeBot, StudentAgent)[0] == Player.PLAYER_TWO

def test_small_world_winner():
    """
    Verifies that the student's agent is able to defeat SnakeBot in the small world.
    """
    w1, p1_acts_1, p2_acts_1 = game_loop("worlds/small.world", StudentAgent, SnakeBot)
    assert w1 == Player.PLAYER_ONE, f"\n[P1 Failed in small.world]\nWinner was: {w1}\nStudentAgent (P1) acts: {p1_acts_1}\nSnakeBot (P2) acts: {p2_acts_1}"

    w2, p1_acts_2, p2_acts_2 = game_loop("worlds/small.world", SnakeBot, StudentAgent)
    assert w2 == Player.PLAYER_TWO, f"\n[P2 Failed in small.world]\nWinner was: {w2}\nSnakeBot (P1) acts: {p1_acts_2}\nStudentAgent (P2) acts: {p2_acts_2}"


def test_medium_world_winner():
    """
    Verifies that the student's agent is able to defeat SnakeBot in the medium world.
    """
    w1, p1_acts_1, p2_acts_1 = game_loop("worlds/medium.world", StudentAgent, SnakeBot)
    assert w1 == Player.PLAYER_ONE, f"\n[P1 Failed in medium.world]\nWinner was: {w1}\nStudentAgent (P1) acts: {p1_acts_1}\nSnakeBot (P2) acts: {p2_acts_1}"

    w2, p1_acts_2, p2_acts_2 = game_loop("worlds/medium.world", SnakeBot, StudentAgent)
    assert w2 == Player.PLAYER_TWO, f"\n[P2 Failed in medium.world]\nWinner was: {w2}\nSnakeBot (P1) acts: {p1_acts_2}\nStudentAgent (P2) acts: {p2_acts_2}"


def test_large_world_winner():
    """
    Verifies that the student's agent is able to defeat SnakeBot in the large world.
    """
    w1, p1_acts_1, p2_acts_1 = game_loop("worlds/large.world", StudentAgent, SnakeBot)
    assert w1 == Player.PLAYER_ONE, f"\n[P1 Failed in large.world]\nWinner was: {w1}\nStudentAgent (P1) acts: {p1_acts_1}\nSnakeBot (P2) acts: {p2_acts_1}"

    w2, p1_acts_2, p2_acts_2 = game_loop("worlds/large.world", SnakeBot, StudentAgent)
    assert w2 == Player.PLAYER_TWO, f"\n[P2 Failed in large.world]\nWinner was: {w2}\nSnakeBot (P1) acts: {p1_acts_2}\nStudentAgent (P2) acts: {p2_acts_2}"