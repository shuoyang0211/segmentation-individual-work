<!--
========================================================================================================================

    This is a Markdown file. If you are using VS Code, right-click this file and select "Open Preview" to render it!
    
========================================================================================================================
-->

# Individual Tasks

| [`README`](/README.md#cs182-individual-programming-assignment-1-segmentation) | [`Installation`](/docs/1-installation.md#installation) | [`Game Overview`](/docs/2-game-overview.md#game-overview) | [`Individual Tasks`] | [`Getting Started`](/docs/4-getting-started.md#getting-started) |
| :---: | :---: | :---: | :---: | :---: |

<br>

Before writing your own policy to play against intelligent agents, you will first defeat a simpler opponent. This initial challenger is `SlothBot`, a naive and lazy agent that always stays in place. For your reference, we've provided some pseudocode in `docs/pseudocode.md`.

1. In [`src/segmentation/agents/dfs_agent.py`](/src/segmentation/agents/dfs_agent.py), implement the `dfs` and `get_action` methods so that your agent navigates from its starting position to `SlothBot`'s position, eliminating `SlothBot`.

2. In [`src/segmentation/agents/bfs_agent.py`](/src/segmentation/agents/bfs_agent.py), implement the `bfs` and `get_action` methods so that your agent navigates from its starting position to `SlothBot`'s position, eliminating `SlothBot`.

3. In [`src/segmentation/agents/a_star_agent.py`](/src/segmentation/agents/a_star_agent.py), implement the `a_star` and `get_action` methods so that your agent navigates from its starting position to `SlothBot`'s position, eliminating `SlothBot`.

> [!tip]
> Before you implement one of these search algorithms, a good first step is to make sure your agent can traverse the board. For example, can you write an agent that picks random moves, while avoiding repeated positions? The `transition` method in `GameState` may be useful for constructing and traversing the game tree. Don't forget that the other player gets an action too!

<br>

A new competitor enters the scene: `SnakeBot`. Unlike our listless initial foe, `SnakeBot` slithers around the grid, extending its trail as long as possible before switching directions. More precisely, `SnakeBot` chooses a direction at random and continues in that direction until it reaches a wall or its own trail. At this point, `SnakeBot` randomly selects a different direction that won't cause it to immediately lose, stopping if no such direction exists.

1. In [`src/segmentation/agents/student_agent.py`](/src/segmentation/agents/student_agent.py), implement the `get_action` method so that your agent beats `SnakeBot`. One strategy is to use a dynamic modification of A\* that handles changing environments (see *dynamic A\**). This is only of many possible strategies, so we encourage you to get creative for this part!

<br>

---

| [<- `Game Overview`](/docs/2-game-overview.md#game-overview) | [`Back to top`](#individual-tasks) | [`Getting Started` ->](/docs/4-getting-started.md#getting-started) |
| :--- | :---: | ---: |
