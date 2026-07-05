<!--
========================================================================================================================

    This is a Markdown file. If you are using VS Code, right-click this file and select "Open Preview" to render it!
    
========================================================================================================================
-->

# Pseudocode

| [`DFS`](#dfs) | [`BFS`](#bfs) | [`A Star`](#a-star) |
| :---: | :---: | :---: |

<br>

This file contains pseudocode for some graph search algorithms from lecture. You are free to use these as baselines for your agent implementations. There are many other (equally valid) ways to implement these algorithms, which you are encouraged to explore.

## `DFS`

```none
function DFS(start_state):
    create an empty stack
    create an empty visited set

    push start_state onto the stack, along with an empty path

    while the stack is not empty:
        remove the most recently added state and path from the stack

        if this state is the goal:
            return the path

        if this state has already been visited:
            continue

        mark this state as visited

        for each successor of this state:
            create a new path by adding this move to the current path
            push the successor and new path onto the stack

    return failure
```

## `BFS`

```none
function BFS(start_state):
    create an empty queue
    create an empty visited set

    add start_state to the queue, along with an empty path
    mark start_state as visited

    while the queue is not empty:
        remove the oldest state and path from the queue

        if this state is the goal:
            return the path

        for each successor of this state:
            if the successor has not been visited:
                mark the successor as visited
                create a new path by adding this move to the current path
                add the successor and new path to the queue

    return failure
```

## `A Star`

```none
function BFS(start_state):
    create an empty queue
    create an empty visited set

    add start_state to the queue, along with an empty path
    mark start_state as visited

    while the queue is not empty:
        remove the oldest state and path from the queue

        if this state is the goal:
            return the path

        for each successor of this state:
            if the successor has not been visited:
                mark the successor as visited
                create a new path by adding this move to the current path
                add the successor and new path to the queue

    return failure
```

<br>

---

| [`Back to top`](#pseudocode) |
| :---: |
