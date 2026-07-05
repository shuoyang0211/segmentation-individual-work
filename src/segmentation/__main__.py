from __future__ import annotations

from argparse import ArgumentParser
from enum import Enum
from time import sleep
from typing import Callable

from segmentation_core import print_centered
from segmentation_core.engine import GameState, Player
from segmentation_core.agents import (
    AgentProtocol,
    ChaserBot,
    SlothBot,
    RandomBot,
    SnakeBot,
    TreeBot,
)
from segmentation.renderer import Renderer
from segmentation.agents import (
    DFSAgent,
    BFSAgent,
    AStarAgent,
    StudentAgent,
    TeleopAgent,
)


class AgentId(str, Enum):
    ASTAR = "astar"
    BFS = "bfs"
    DFS = "dfs"
    CHASER = "chaser"
    RANDOM = "random"
    STUDENT = "student"
    TELEOP = "teleop"
    TREE = "tree"
    SLOTH = "sloth"
    SNAKE = "snake"


AGENT_REGISTRY: dict[AgentId, Callable[..., AgentProtocol]] = {
    AgentId.ASTAR: AStarAgent,
    AgentId.BFS: BFSAgent,
    AgentId.DFS: DFSAgent,
    AgentId.CHASER: ChaserBot,
    AgentId.RANDOM: RandomBot,
    AgentId.STUDENT: StudentAgent,
    AgentId.TELEOP: TeleopAgent,
    AgentId.SLOTH: SlothBot,
    AgentId.SNAKE: SnakeBot,
    AgentId.TREE: TreeBot,
}


def get_agent(agent_id: AgentId, **kwargs) -> AgentProtocol:
    try:
        return AGENT_REGISTRY[agent_id](**kwargs)
    except KeyError:
        choices = ", ".join(a.value for a in AgentId)
        raise ValueError(f"Unknown agent ID: {agent_id!s}. Choices: {choices}")


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--world",
        type=str,
        default="worlds/small.world",
        help="path to world file to load"
    )
    parser.add_argument(
        "--agent-one",
        type=AgentId,
        choices=[a.value for a in AgentId],
        default=AgentId.TELEOP,
        help="which agent to use for player one"
    )
    parser.add_argument(
        "--agent-two",
        type=AgentId,
        choices=[a.value for a in AgentId],
        default=AgentId.TELEOP,
        help="which agent to use for player two"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="render board to terminal instead of a GUI"
    )
    parser.add_argument(
        "--render-delay",
        type=float,
        default=0.02,
        help="delay between frames (in seconds). useful when running two autonomous agents"
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=250,
        help="max number of iterations before declaring a draw. use -1 for no limit")
    args = parser.parse_args()

    agent_one = get_agent(args.agent_one, side=Player.PLAYER_ONE)
    agent_two = get_agent(args.agent_two, side=Player.PLAYER_TWO)
    game_state = GameState(args.world, max_iterations=args.max_iterations if args.max_iterations >= 0 else None)
    renderer = Renderer()

    while game_state.winner is None:
        if args.headless:
            print_centered(str(game_state))
        else:
            renderer.render(game_state)

        active_agent = (
            agent_one if game_state.active_player == Player.PLAYER_ONE else agent_two
        )
        action = active_agent.get_action(game_state)
        game_state = game_state.transition(action)

        sleep(args.render_delay)

    print(f"Winner: {game_state.winner}")
    if args.headless:
        print_centered(str(game_state))
    else:
        renderer.render(game_state)

    while True:
        renderer.render(game_state)


if __name__ == "__main__":
    main()
