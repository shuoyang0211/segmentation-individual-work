from collections.abc import Callable
import heapq
import itertools

from segmentation_core.engine import Action, GameState, Player


class AStarAgent:
    def __init__(self, side: Player):
        self._name = "A* Agent"
        self._side = side
        self._plan = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def a_star(self, state: GameState, heuristic: Callable[[GameState], float]):
        """
        Task 3: Implement the A* search algorithm on the game tree to determine
        a sequence of actions that gets your agent to SlothBot.

        Parameters:
            `state`: The current state of the game.
            `heuristic`: A cost-to-go heuristic for game states.

        Note:
            You can assume that SlothBot is stationary and always reachable.
        """
        target_pos = state.get_player_state(self.side.other()).position
        start_pos = state.get_player_state(self.side).position

        # Initialization: create an empty priority queue
        pq = []
        # When the priorities are the same, FIFO
        tie_breaker = itertools.count()

        # Initialization: create a map storing the best known cost to each state
        best_cost = {start_pos: 0}

        initial_f = 0 + heuristic(state)
        heapq.heappush(pq, (initial_f, next(tie_breaker), 0, state, []))

        # 5. while the priority queue is not empty:
        while pq:
            # remove the state with the lowest priority
            f_score, _, g_cost, curr_state, path = heapq.heappop(pq)
            my_pos = curr_state.get_player_state(self.side).position

            # if this state is the goal: return the path
            if my_pos == target_pos:
                return path

            # If the game ends due to the exhaustion of the turns
            if curr_state.winner is not None:
                continue

            if g_cost > best_cost.get(my_pos, float("inf")):
                continue

            # for each successor of this state:
            for action in [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT]:
                next_state = curr_state.transition(action)

                if next_state.winner == self.side.other():
                    continue

                if next_state.winner is None:
                    next_state = next_state.transition(Action.STAY)

                next_pos = next_state.get_player_state(self.side).position
                new_cost = g_cost + 1  

                # if successor has not been seen before or new_cost is better:
                if next_pos not in best_cost or new_cost < best_cost[next_pos]:
                    # update the best known cost to successor
                    best_cost[next_pos] = new_cost

                    # priority = new_cost + heuristic(successor)
                    priority = new_cost + heuristic(next_state)

                    # create a new path and add to priority queue
                    new_path = path + [action]
                    heapq.heappush(
                        pq,
                        (priority, next(tie_breaker), new_cost, next_state, new_path)
                    )

        return []

    def squared_euclidean_heuristic(self, state: GameState) -> float:
        """
        Calculates the squared Euclidean distance from the agent to SlothBot.
        h(n) = (dx)^2 + (dy)^2
        """
        my_pos = state.get_player_state(self.side).position
        target_pos = state.get_player_state(self.side.other()).position
        dx = my_pos[0] - target_pos[0]
        dy = my_pos[1] - target_pos[1]
        return float(dx**2 + dy**2)
    
    def get_action(self, state: GameState) -> Action:
        """
        Computes the next action to take based on the given game state.

        Parameters:
            `state`: The current state of the game.

        Returns:
            The next action to take to move towards SlothBot.

        Note:
            For your final submission to Gradescope, make sure to use
            squared Euclidean distance as your heuristic function.
        """
        if not self._plan:
            self._plan = self.a_star(state, self.squared_euclidean_heuristic)

        if self._plan:
            return self._plan.pop(0)

        return Action.STAY
