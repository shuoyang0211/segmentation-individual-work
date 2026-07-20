<!--
========================================================================================================================

    This is a Markdown file. If you're using VS Code, right-click the filename and select "Open Preview" to render it!

========================================================================================================================
-->

# CS 1820 Individual Programming Assignment 1: Segmentation

| [`README`] | [`Installation`](/docs/1-installation.md#installation) | [`Game Overview`](/docs/2-game-overview.md#game-overview) | [`Getting Started`](/docs/3-getting-started.md#getting-started) | [`Individual Tasks`](/docs/4-individual-tasks.md#tasks) |
| :---: | :---: | :---: | :---: | :---: |

<br>

Welcome to the CS 1820 Arcade! Over the course of the semester, we'll be taking a deeper dive into many of the topics covered in lecture through individual and group programming assignments. In particular, we will apply the knowledge you've learned in class to plan and train agents for games.

For this series of assignments, you'll be implementing various agents for a two-player turn-based strategy game. We're especially interested in diving deep into the topic of adversarial search. To get started, we have split this `README` into a series of Markdown files, which you can navigate through at the top. We highly recommend reading through the entire assignment and the stencil code before you start working.

<figure style="text-align: center;">
    <img src="./docs/imgs/game_preview.gif" alt="Player 1 defeats Player 2." width="400">
</figure>

<br>

## Code Structure

This repository contains five major directories of interest.

### `docs/`

In addition to the files in this `README`, we've provided a few handouts for your reference.

- `comments.md` contains documentation for important classes related to the game.
- `pseudocode.md` contains high-level pseudocode for some of the algorithms we learned in class.

### `scripts/`

We've also created a few helpful scripts to aid in the development of your agents.

- `creator.py` provides a simple GUI to edit existing worlds and create new worlds, which you can use to test your agents. Once your project environment is set up, you can run `uv run scripts/creator.py -h` for more details.

### `src/`

All code that you will be responsible for belongs here. In particular, you will be implementing various agents that will face off against bots provided by the TAs. In general, refrain from making *destructive* edits to the stencil code to ensure compatibility with the autograder. Adding new files, functions, and methods is encouraged! External third-party dependencies are not allowed, but feel free to import any built-in Python module.

As you work through this assignment, you may want to examine the exports of the `segmentation_core` package, which contains all the game logic for this assignment. You can view documentation for relevant classes, methods, and functions with the following methods.

- Locate and view their type stubs directly in your IDE. These can be found at `.venv/lib/segmentation_core/`. Alternatively, if you're using VS Code, you can `Ctrl`/`Cmd` + `Click` on the package itself or on an object like `Player`.
- Import the package in a Python REPL, and call `help(object)` on your desired class, method, or function.

Some of these comments have been replicated at `docs/comments.md` for your convenience. If you have any questions about how any part of this assignment works, please feel free to post a question on [Ed](TODO)!

### `tests/`

We've provided some simple tests for you to debug your implementations before submitting to Gradescope. The tests in your handout are a strict subset of those used by our autograder. You can run these local tests by executing `uv run pytest`. We recommend that you write your own tests as well!

### `worlds/`

All the TA-provided world files used for the local tests are located in this folder. In addition to some basic worlds and "path" worlds used for testing, we have also provided a number of "expansion" worlds to play around with as you implement your own agent. To stay organized, we recommend that you save your custom world files in this folder.

<br>

---

| [`Back to top`](#cs-1820-individual-programming-assignment-1-segmentation) | [`Installation` ->](/docs/1-installation.md#installation) |
| :---: | ---: |
