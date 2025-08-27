from __future__ import annotations

from argparse import ArgumentParser
from enum import StrEnum
from time import sleep
from typing import Callable

from segmentation_core import print_centered
from segmentation_core.engine import GameState, Player
from segmentation_core.agents import AgentProtocol, ChaserBot, SlothBot, RandomBot, VoronoiBot, TreeBot
from segmentation.agents import BFSAgent, DFSAgent, DynamicAStarAgent, StaticAStarAgent, TeleopAgent
from segmentation.renderer import render

class AgentId(StrEnum):
    BFS           = "bfs"
    DFS           = "dfs"
    CHASER        = "chaser"
    DYNAMIC_ASTAR = "dynamic_astar"
    RANDOM        = "random"
    STATIC_ASTAR  = "static_astar"
    TELEOP        = "teleop"
    TREE          = "tree"
    VORONOI       = "voronoi"
    SLOTH         = "sloth"

AGENT_REGISTRY: dict[AgentId, Callable[..., AgentProtocol]] = {
    AgentId.BFS:           BFSAgent,
    AgentId.DFS:           DFSAgent,
    AgentId.CHASER:        ChaserBot,
    AgentId.DYNAMIC_ASTAR: DynamicAStarAgent,
    AgentId.RANDOM:        RandomBot,
    AgentId.STATIC_ASTAR:  StaticAStarAgent,
    AgentId.TELEOP:        TeleopAgent,
    AgentId.TREE:          TreeBot,
    AgentId.VORONOI:       VoronoiBot,
    AgentId.SLOTH:         SlothBot,
}

def get_agent(agent_id: AgentId, **kwargs) -> AgentProtocol:
    try:
        return AGENT_REGISTRY[agent_id](**kwargs)
    except KeyError:
        choices = ", ".join(a.value for a in AgentId)
        raise ValueError(f"Unknown agent id: {agent_id!s}. Choices: {choices}")

def main() -> None:
    parser = ArgumentParser()
    parser.add_argument("--world", type=str, default="worlds/small.world")
    parser.add_argument("--agent-one", type=AgentId, choices=list(AgentId), default=AgentId.TELEOP)
    parser.add_argument("--agent-two", type=AgentId, choices=list(AgentId), default=AgentId.TELEOP)
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--render-delay", type=float, default=0.0)
    args = parser.parse_args()

    agent_one = get_agent(args.agent_one, side=Player.PLAYER_ONE)
    agent_two = get_agent(args.agent_two, side=Player.PLAYER_TWO)
    game_state = GameState(args.world)

    while game_state.winner is None:
        if args.headless:
            print_centered(str(game_state))
        else:
            render(game_state)

        active_agent = agent_one if game_state.active_player == Player.PLAYER_ONE else agent_two
        action = active_agent.get_action(game_state)
        game_state = game_state.transition(action)

        sleep(args.render_delay)

    print(f"Winner: {game_state.winner}")
    if args.headless:
        print_centered(str(game_state))
    else:
        render(game_state)

    input("Press enter to exit...")

if __name__ == "__main__":
    main()
