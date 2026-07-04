<!--
========================================================================================================================

    This is a Markdown file. If you are using VS Code, right-click this file and click "Open Preview" to render it!
    
========================================================================================================================
-->

# Getting Started

| [`README`](/README.md#cs182-individual-programming-assignment-1-segmentation) | [`Installation`](/docs/1-installation.md#installation) | [`Game Overview`](/docs/2-game-overview.md#game-overview) | [`Individual Tasks`](/docs/3-individual-tasks.md#individual-tasks) | [`Getting Started`] |
| :---: | :---: | :---: | :---: | :---: |

<br>

#### Running the code

To run the starter code use:

```
uv run segmentation [--help] [--world WORLD] [--agent-one AGENT_ID] [--agent-two AGENT_ID] [--headless] [--render-delay]
```

To run the provided tests (or ones you created) use:

```
uv run pytest
```

> [!NOTE]
> No sourcing required! If you prefer the virtual environment folder to not be called `.venv` then you can pass a name to the `uv venv` command. However, this would require setting the `UV_PROJECT_ENVIRONMENT` variable to this name either prior to every `uv sync` and `uv run` command, exporting the variable in every terminal session, or using some external dependency to manage your environment variables like [`direnv`](https://direnv.net/).

## Tips and Debugging

We use `pytest` to write and run tests for your assignments. `pytest` comes with a ton of handy and useful flags to help you test and debug parts of your code! Here's a list of useful flags to pass to `pytest` when debugging your assignment.

### Selecting Tests

```
pytest                      # run all tests (auto-discovery)
pytest path/                # run tests under a directory
pytest tests/test_x.py      # run tests in a file
```

### Failure Control

```
pytest -x                  # stop after first failure
pytest --maxfail=3         # stop after 3 failures
pytest --lf                # run last-failed tests only
pytest --ff                # run failures first, then the rest
pytest --sw                # stepwise: stop on first fail, resume next time
```

### Output

```
pytest -q                  # quiet (less output)
pytest -v                  # verbose (test names)
pytest -vv                 # extra verbose
pytest -s                  # don't capture stdout/stderr (show prints)
pytest -rA                 # show summary for all outcomes (reasons)
pytest -l                  # show local variables in tracebacks
pytest --tb=short          # shorter tracebacks
pytest --tb=line           # one-line tracebacks
pytest --durations=10      # show 10 slowest tests
```

### Common Combinations

```
# Fail fast with clear reasons
pytest -x -vv -rA --tb=short

# Re-run only what failed last time, show prints
pytest --lf -s -vv

# Redirecting output to a file for readability
pytest -s > foo.txt
```

<br>

---

| [← `Individual Tasks`](/docs/3-individual-tasks.md#individual-tasks) | [`Back to top`](#getting-started) |
| :--- | :---: |
