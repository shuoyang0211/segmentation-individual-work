from segmentation_core.engine import Action, GameState, Player


class DFSAgent:
    def __init__(self, side: Player):
        self._name = "DFS Agent"
        self._side = side
        self._plan = []

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def dfs(self, state: GameState):
        """
        Task 1: Implement depth-first search on the game tree to determine
        a sequence of actions that gets your agent to SlothBot.

        Parameters:
            `state`: The current state of the game.

        Note:
            You can assume that SlothBot is stationary and always reachable.
        """
        # Initialization: create an empty stack
        # push start_state onto the stack, along with an epmty path
        stack = [(state, [])]

        # Initialization: create an empty visit set
        visited = set()

        # Lock SlothBot's physical coordinates at the starting point
        target_pos = state.get_player_state(self.side.other()).position

        # while the stack is not empty:
        while stack:
            # remove the most recently added state and path from the stack (LIFO)
            curr_state, path = stack.pop()
            my_pos = curr_state.get_player_state(self.side).position

            # if current state is the goal, return the path
            if my_pos == target_pos:
                return path 
            
            if curr_state.winner is not None:
                continue
            
            # if this state has already been visited: continue
            if my_pos in visited:
                continue

            # mark this state as visited
            visited.add(my_pos)

            # travel each successor of this state
            for action in [Action.RIGHT, Action.UP, Action.LEFT, Action.DOWN]:
                next_state = curr_state.transition(action)
                if next_state.winner is None:
                    # simulate the slothbot's action
                    next_state = next_state.transition(Action.STAY)
                
                # create a new path by adding this move to the current path
                # push the successor and new path onto the stack
                stack.append((next_state, path + [action]))

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
            self._plan = self.dfs(state)

        if self._plan:
            return self._plan.pop(0)
        
        return Action.STAY
