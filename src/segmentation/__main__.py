from __future__ import annotations

from argparse import ArgumentParser
from collections.abc import Callable
from enum import Enum

from segmentation_core import run
from segmentation_core.agents import (
    AgentProtocol,
    ChaserBot,
    RandomBot,
    SlothBot,
    SnakeBot,
    TreeBot,
)
from segmentation_core.engine import Player

from segmentation.agents import (
    AStarAgent,
    BFSAgent,
    DFSAgent,
    StudentAgent,
)


class AgentId(str, Enum):
    A_STAR = "a_star"
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
    AgentId.A_STAR: AStarAgent,
    AgentId.BFS: BFSAgent,
    AgentId.DFS: DFSAgent,
    AgentId.CHASER: ChaserBot,
    AgentId.RANDOM: RandomBot,
    AgentId.STUDENT: StudentAgent,
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


def resolve_agent(agent_id: AgentId, side: Player, headless: bool) -> AgentProtocol | str:
    """Like `get_agent`, but handles teleop, which isn't a constructible AgentProtocol object.

    Teleop is driven by Bevy's own keyboard input inside the GUI window, so it's passed
    through to `run` as the literal string "teleop" rather than an agent instance.
    """
    if agent_id == AgentId.TELEOP:
        if headless:
            raise ValueError("the teleop agent requires the GUI; rerun without --headless")
        return "teleop"
    return get_agent(agent_id, side=side)


def main() -> None:
    parser = ArgumentParser()
    parser.add_argument(
        "--world",
        type=str,
        default="worlds/small.world",
        help="Path to a world file.",
    )
    parser.add_argument(
        "--agent-one",
        type=AgentId,
        choices=[a.value for a in AgentId],
        default=AgentId.TELEOP,
        help="Which agent to use for player one.",
    )
    parser.add_argument(
        "--agent-two",
        type=AgentId,
        choices=[a.value for a in AgentId],
        default=AgentId.TELEOP,
        help="Which agent to use for player two.",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Optionally render board to terminal instead of as a GUI.",
    )
    parser.add_argument(
        "--marching-squares",
        action="store_true",
        help="Optionally render tiles as smoothed blobs.",
    )
    parser.add_argument(
        "--render-delay",
        type=int,
        default=20,
        help="Delay between frames (in seconds). Useful when running two autonomous agents.",
    )
    parser.add_argument(
        "--max-iterations",
        type=int,
        default=0,
        help="Max iterations before declaring a draw. Use 0 for no limit.",
    )
    args = parser.parse_args()

    agent_one = resolve_agent(args.agent_one, Player.PLAYER_ONE, args.headless)
    agent_two = resolve_agent(args.agent_two, Player.PLAYER_TWO, args.headless)
    max_iterations = args.max_iterations if args.max_iterations > 0 else None

    run(
        args.world,
        agent_one,
        agent_two,
        max_iterations,
        args.render_delay,
        args.headless,
        args.marching_squares,
    )


if __name__ == "__main__":
    main()
