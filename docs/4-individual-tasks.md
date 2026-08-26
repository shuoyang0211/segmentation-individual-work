<!--
========================================================================================================================

    This is a Markdown file. If you're using VS Code, right-click the filename and select "Open Preview" to render it!

========================================================================================================================
-->

# Individual Tasks

| [`README`](../README.md#cs-1820-individual-programming-assignment-1-segmentation) | [`Installation`](1-installation.md#installation) | [`Game Overview`](2-game-overview.md#game-overview) | [`Getting Started`](3-getting-started.md#getting-started) | [`Individual Tasks`] |
| :---: | :---: | :---: | :---: | :---: |

<br>

Before writing your own policy to play against smarter agents, you will first use some classic search algorithms to defeat a simpler opponent. Your initial challenger is `SlothBot`, a naive agent that always stays in place. To check that your agents have the expected behavior, you can run our provided tests (or run your own tests!) with `pytest`. We've also provided some pseudocode in `docs/pseudocode.md`.

1. In [`agents/dfs_agent.py`](../src/segmentation/agents/dfs_agent.py), implement the `dfs` and `get_action` methods so that your agent navigates from its starting position to `SlothBot`'s position, eliminating `SlothBot`.

2. In [`agents/bfs_agent.py`](../src/segmentation/agents/bfs_agent.py), implement the `bfs` and `get_action` methods so that your agent navigates from its starting position to `SlothBot`'s position, eliminating `SlothBot`.

3. In [`agents/a_star_agent.py`](../src/segmentation/agents/a_star_agent.py), implement the `a_star` and `get_action` methods so that your agent navigates from its starting position to `SlothBot`'s position, eliminating `SlothBot`. Feel free to play around with different heuristic functions, but for the final submission, we ask that you use [*squared* Euclidean distance](https://en.wikipedia.org/wiki/Euclidean_distance#Squared_Euclidean_distance). (Is this an *admissible* heuristic?)

> [!tip]
> Before implementing a complex search algorithm, a good first step is to make sure your agent is able to move around. For example, can you write an agent that picks random moves, while avoiding repeated positions? The `transition` method in `GameState` may be useful for constructing and traversing the game tree. Don't forget that the other player gets an action too!

<br>

A new competitor enters the scene: `SnakeBot`. Unlike our lazier first foe, `SnakeBot` slithers around the grid, extending its trail as long as possible before switching directions. More precisely, `SnakeBot` chooses a direction at random and continues in that direction until it reaches a wall or its own trail. At this point, `SnakeBot` randomly selects a different direction that won't cause it to immediately lose, stopping if no such direction exists.

4. In [`agents/student_agent.py`](../src/segmentation/agents/student_agent.py), implement the `get_action` method so that your agent beats `SnakeBot`. One strategy is to use a dynamic modification of A\* that handles changing environments (see [dynamic A\*](https://en.wikipedia.org/wiki/D*)). This is only of many possible strategies, so we encourage you to get creative for this part!

<br>

---

| [← `Getting Started`](3-getting-started.md#getting-started) | [`Back to top`](#individual-tasks) |
| :--- | :---: |
