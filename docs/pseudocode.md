<!--
========================================================================================================================

    This is a Markdown file. If you're using VS Code, right-click the filename and select "Open Preview" to render it!

========================================================================================================================
-->

# Pseudocode

| [`DFS`](#dfs) | [`BFS`](#bfs) | [`A Star`](#a-star) |
| :---: | :---: | :---: |

<br>

This file contains pseudocode for some graph search algorithms from lecture. You are free to use these as baselines for your agent implementations. There are many other (equally valid) ways to implement these algorithms, which you are encouraged to explore.

## `DFS`

```none
function dfs(start_state):
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
function bfs(start_state):
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
function a_star(start_state):
    create an empty priority queue
    create a map storing the best known cost to each state

    add start_state to the priority queue with priority 0
    record that the cost to reach start_state is 0

    while the priority queue is not empty:
        remove the state with the lowest priority

        if this state is the goal:
            return the path

        for each successor of this state:
            new_cost = cost_so_far_to_current_state + cost_to_successor

            if successor has not been seen before
               or new_cost is better than the best known cost to successor:

                update the best known cost to successor

                priority = new_cost + heuristic(successor)

                create a new path by adding this move to the current path
                add the successor and new path to the priority queue with this priority

    return failure
```

<br>

---

| [`Back to top`](#pseudocode) |
| :---: |
