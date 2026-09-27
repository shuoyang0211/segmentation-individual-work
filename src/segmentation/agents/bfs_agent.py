from segmentation_core.engine import Action, GameState, Player
from collections import deque


class BFSAgent:
    def __init__(self, side: Player):
        self._name = "BFS Agent"
        self._side = side
        self._plan = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    # A version fine-tuned from the dfs function:
    # The higher space complexity of BFS may lead to a crash

    # def bfs(self, state: GameState):
    #     """
    #     Task 2: Implement breadth-first search on the game tree to determine
    #     a sequence of actions that gets your agent to SlothBot.

    #     Parameters:
    #         `state`: The current state of the game.

    #     Note:
    #         You can assume that SlothBot is stationary and always reachable.
    #     """
    #     # Initialization: create an empty queue
    #     queue = deque([(state, [])])

    #     # Initialization: create an empty visit set
    #     start_pos = state.get_player_state(self.side).position
    #     visited = {start_pos}

    #     # Lock SlothBot's physical coordinates at the starting point
    #     target_pos = state.get_player_state(self.side.other()).position

    #     # while the queue is not empty:
    #     while queue:
    #         # remove the oldest state and path from the queue (FIFO)
    #         curr_state, path = queue.popleft()
    #         my_pos = curr_state.get_player_state(self.side).position

    #         # if current state is the goal, return the path
    #         if my_pos == target_pos:
    #             return path 

    #         # travel each successor of this state
    #         for action in [Action.RIGHT, Action.UP, Action.LEFT, Action.DOWN]:
    #             next_state = curr_state.transition(action)

    #             if next_state.winner == self.side.other():
    #                 continue

    #             if next_state.winner is None:
    #                 # simulate the slothbot's action
    #                 next_state = next_state.transition(Action.STAY)
                
    #             next_pos = next_state.get_player_state(self.side).position
                
    #             # if the successor has not been visited:
    #             if next_pos not in visited:
    #                 # mark the successor as visited
    #                 visited.add(next_pos)

    #             # create a new path by adding this move to the current path
    #             # push the successor and new path into the queue
    #             queue.append((next_state, path + [action]))

    #     return []

    # Due to the optimal and complete properties of BFS, the function can be simplified
    
    def bfs(self, state: GameState):
        """
        Task 2: Implement breadth-first search on the game tree.
        (Simplified Geometric Version for Maximum Performance)
        """
        board = state.board
        start_pos = state.get_player_state(self.side).position
        target_pos = state.get_player_state(self.side.other()).position

        queue = deque([(start_pos, [])])
        visited = {start_pos}

        # Just perform the basic addition and subtraction
        # skipping the engine physics simulation
        directions = {
            Action.UP: (0, -1),
            Action.DOWN: (0, 1),
            Action.LEFT: (-1, 0),
            Action.RIGHT: (1, 0)
        }

        while queue:
            (x, y), path = queue.popleft()

            if (x, y) == target_pos:
                return path

            for action, (dx, dy) in directions.items():
                nx, ny = x + dx, y + dy
                next_pos = (nx, ny)

                # 1. Border check: Must not go beyond the map boundaries
                if nx < 0 or nx >= board.width or ny < 0 or ny >= board.height:
                    continue
                
                # 2. Obstacle check: Must avoid colliding with walls
                if next_pos in board.walls:
                    continue

                # 3. Duplicate check: Pre-marking before enqueue in BFS standard
                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [action]))

        return []

    def get_action(self, state: GameState) -> Action:
        """
        Computes the next action to take based on the given game state.

        Parameters:
            `state`: The current state of the game.

        Returns:
            The next action to take to move towards SlothBot.
        """
        if not self._plan:
            self._plan = self.bfs(state)

        if self._plan:
            return self._plan.pop(0)
        
        return Action.STAY
