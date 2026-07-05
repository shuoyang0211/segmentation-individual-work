<!--
========================================================================================================================

    This is a Markdown file. If you are using VS Code, right-click this file and select "Open Preview" to render it!
    
========================================================================================================================
-->

# Getting Started

| [`README`](/README.md#cs182-individual-programming-assignment-1-segmentation) | [`Installation`](/docs/1-installation.md#installation) | [`Game Overview`](/docs/2-game-overview.md#game-overview) | [`Individual Tasks`](/docs/3-individual-tasks.md#individual-tasks) | [`Getting Started`] |
| :---: | :---: | :---: | :---: | :---: |

<br>

Now, you should be ready to start implementing your own agents and testing them out! In this file, we will introduce the various programs which you will need as you complete the assignment. We have also added some more info about using Git, which can save you from a lot of future headaches. Git will be especially useful for the group portion.

<br>

## Running code

### Using `segmentation`

To run the starter code, you can use the following command.

```sh
uv run segmentation [--help] [--world WORLD] [--agent-one AGENT_ID] [--agent-two AGENT_ID] [--headless] [--render-delay]
```

> [!tip]
> The items in square brackets `[]` are optional arguments called *flags*, which allow you to modify the program's behavior. The capitalized phrases are custom inputs. For example, if you want to play with a keyboard-controlled agent against your BFS agent, you can run the following.
> 
> ```sh
> uv run segmentation --agent-one teleop --agent-two bfs
> ```
> 
> You can read about what each flag does by running with the `--help` flag, or its shorthand `-h`.

### Viewing and editing worlds

If you want to try making your own worlds, you can open the board editor GUI by running the following.

```sh
uv run creator.py [--help] (--load LOAD | --size SIZE) [--cell CELL] [--out OUT] [--no-grid] [--palette-right] [--title TITLE]
```

> [!tip]
> The `--load` flag opens an existing world, while the `--size` flag creates a new world. Here, the parentheses `()` indicate that exactly one of these needs to be supplied in order to run the program. Again, you can read about each option by using the `-h` flag.

### Testing your code

We use [`pytest`](https://docs.pytest.org/en/stable/) to write and run tests for your assignments. To run our provided tests (or your own custom tests), use the following.

```sh
uv run pytest
```

### Debugging tips

`pytest` comes with a *ton* of flags to help you test and debug your code. Here, we have listed only a few flags that you may find useful.

> <details><summary><b>Selecting tests</b></summary>
> 
> ```sh
> pytest                      # run all tests (auto-discovery)
> pytest <custom_tests/>      # run tests under a directory
> pytest <tests/test_x.py>    # run tests in a file
> ```
> 
> </details>

> <details><summary><b>Failure control</b></summary>
> 
> ```sh
> pytest -x                   # stop after first failure
> pytest --maxfail=3          # stop after 3 failures
> pytest --lf                 # run last-failed tests only
> pytest --ff                 # run previous failures first, then the rest
> pytest --sw                 # stepwise (stop on first fail, resume next time)
> ```
> 
> </details>

> <details><summary><b>Adjusting the output</b></summary>
> 
> ```sh
> pytest -q                   # quiet (less output)
> pytest -v                   # verbose (show each test)
> pytest -vv                  # very verbose (show untruncated outputs)
> pytest -s                   # don't capture stdout/stderr (i.e., show prints)
> pytest -rA                  # show summary for all outcomes
> pytest -l                   # show local variables in tracebacks
> pytest --tb=short           # shorter tracebacks
> pytest --tb=line            # one-line tracebacks
> pytest --durations=10       # show 10 slowest tests
> ```
> 
> </details>

> <details><summary><b>Common flag combinations</b></summary>
> 
> ```sh
> pytest -x -vv -rA --tb=short    # fail fast with max verbosity and condensed traces
> pytest --lf -s -vv              # rerun only what failed last time, and show prints
> pytest -s > <output.txt>        # redirect prints to a file for readability
> ```
> 
> </details>

<br>

## More about Git

### Managing versions with Git

[Git](https://git-scm.com/) is actually something called a *distributed version control system*, which is to grossly simplify, a piece of software used by developers to manage different versions of their code. You can learn more about what that means and how to start using it by reading this [amazing introduction](https://cs61.seas.harvard.edu/site/2025/git/) from Prof. Eddie Kohler. You can also find a number of guides online if you want to learn more.

In a nutshell, Git allows you to *commit* snapshots of your project, and the entire history of commits is saved in your repository. Not only does this save your current progress, it also lets you view past versions of your code and revert changes without losing any data. Some commands that are worth looking into as you start the assignment are `status`, `add`, `commit`, `log`, `diff`, `push`, and `pull`. If you only remember one thing about Git, remember to ***commit early and often***!

### Common Git workflow

The following is the most common Git workflow.

```sh
git pull                        # fetch changes in the remote repo and merge them into your local repo
git add .                       # begin tracking new files and stage all changes in your local repo
git commit -m "<your message>"  # save a snapshot of your staged changes in your local repo history
git push                        # upload your commits to the remote repo
```

This logs all current changes to your project in a new commit, which you and others can view in the remote repository's webpage. Importantly, you should *always* make sure your code is up-to-date with the remote, by `pull`-ing before `push`-ing any new changes. The `pull` command won't matter for the individual portion of the assignment, but it will be necessary for the group portion.

### Group programming with Git

While Git is useful for coding alone (and fetching homework assignments), where Git really shines is when many, many developers need to work together on the same codebase. You will still independently write code in your local repository. However, you can then `pull` changes that other people have made, and `push` changes for others to see. The workflow above is still the gold standard. If you are interested, you can look into the `branch`, `switch`, and `merge` commands.

### Group programming with Live Share

Another way to code with a small group of people is with the [Live Share](vscode:extension/MS-vsliveshare.vsliveshare) extension from Microsoft. This extension lets you share a single development environment with your group members in real time, which can be a convenient alternative if your group plans to code synchronously. Follow the installation and quickstart guides on the extension page to get started.

<br>

---

| [<- `Individual Tasks`](/docs/3-individual-tasks.md#individual-tasks) | [`Back to top`](#getting-started) |
| :--- | :---: |
