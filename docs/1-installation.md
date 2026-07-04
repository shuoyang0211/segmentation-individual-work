<!--
========================================================================================================================

    This is a Markdown file. If you are using VS Code, right-click this file and click "Open Preview" to render it!
    
========================================================================================================================
-->

# Installation

| [`README`](/README.md#cs182-individual-programming-assignment-1-segmentation) | [`Installation`] | [`Game Overview`](/docs/2-game-overview.md#game-overview) | [`Individual Tasks`](/docs/3-individual-tasks.md#individual-tasks) | [`Getting Started`](/docs/4-getting-started.md#getting-started) |
| :---: | :---: | :---: | :---: | :---: |

<br>

Before we get started with the game, we will walk through how to install `git` and VS Code, clone this repository, install project dependencies with `uv`, and finally start running the game. Feel free to skip any steps if you have done this before.


### `git`

### `uv`

#### Installing `uv`

A headache-free way to start running the starter code is via the [`uv`](https://docs.astral.sh/uv/getting-started/installation/) package manager. To install (on Mac, Linux, WSL):

```
curl -LsSf https://astral.sh/uv/install.sh | sh
```

> [!NOTE]
> The above command requires `curl` installed! You'll most likely have this installed, already but if not it should be a small `brew/apt/pacman install` away. Alternatively, if you have `wget` already installed you can use
>
> ```
> wget -qO- https://astral.sh/uv/install.sh | sh
> ```

Alternative approaches exist to install `uv` which you are invited to explore in the [Astral documentation](https://docs.astral.sh/uv/getting-started/installation/).

#### Installing Project Dependencies

One of the major superpowers of `uv` is its ability to manage different versions of Python using a combination of virtual environments and configuration files. Initialize this project's virtual environment and install all the required dependencies using

```
uv sync
```

This should install an appropriate Python version (3.13) and all the project's dependencies including `pytest`.

### Selecting your Python Interpreter

Using typed Python can highly improve your programming (and especially your debugging experience). To enable type checking in VS Code:

-   Open Settings (`CTRL`/`CMD` + `,`)
-   Search for `Type Checking Mode`
-   Set the mode to your desired level of strictness (`standard` is a good default!)

<div align="center">
    <img src="docs/imgs/type_checking.png" width="1000"/>
</div>

To ensure that all the type stubs are resolved for your installed dependencies, you have to select the correct Python interpreter. To do so:

-   Open the Command Pallette (`CTRL`/`CMD` + `SHIFT` + `P`)
-   Type and select `Python: Select Interpreter`
-   Choose the virtual environment located in the stencil directory.

<div align="center">
    <img src="docs/imgs/interpreter_selection.png" width="1000"/>
</div>

For this to be correctly detected, be sure that the opened folder in VS Code is your cloned GitHub repository!

<br>

---

| [← `README`](/README.md#cs182-individual-programming-assignment-1-segmentation) | [`Back to top`](#installation) | [`Game Overview` →](/docs/2-game-overview.md#game-overview) |
| :--- | :---: | ---: |
