from segmentation_core.engine import Action, GameState, Player
from collections import deque
import heapq
import itertools


class StudentAgent:
    def __init__(self, side: Player):
        self._name = "Student Agent"
        self._side = side

    @property
    def name(self) -> str:
        return self._name

    @property
    def side(self) -> Player:
        return self._side

    def get_action(self, state: GameState) -> Action:
        """
        Computes the next action to take based on the given game state.

        Parameters:
            `state`: The current state of the game.

        Returns:
            The next action to take to move towards SnakeBot.
        """
        my_state = state.get_player_state(self.side)
        enemy_state = state.get_player_state(self.side.other())

        my_trail = my_state.trail
        my_claims = my_state.claims

        enemy_pos = enemy_state.position
        enemy_trail = enemy_state.trail

        board = state.board

        targets = set()

        # 1. Attack: Target the enemy's trajectory and the enemy itself
        if enemy_trail:
            targets.update(enemy_trail)
            targets.add(enemy_pos)
            
        # 2. Defense: Close the trajectory as early as possible to avoid leaving a long trail
        elif len(my_trail) >= 5:
            targets.update(my_claims)
            
        # Grow: Gradually occupying more tiles when there's no opportunity
        else:
            all_tiles = {(x, y) for x in range(board.width) for y in range(board.height)}
            unclaimed_tiles = all_tiles - set(board.walls) - set(my_claims)
            targets.update(unclaimed_tiles)

        # avoid the "danger zone"
        # action = self.dynamic_bfs(state, targets, enemy_pos, enemy_trail)
        action = self.dynamic_a_star(state, targets, enemy_pos, enemy_trail)

        if action is not None:
            return action

        if len(my_trail) == 0:
            return Action.STAY
            
        return self.get_safe_fallback_move(state, enemy_pos, enemy_trail)

    def dynamic_bfs(self, state: GameState, targets: set, enemy_pos: tuple, enemy_trail: set) -> Action | None:
        board = state.board
        my_pos = state.get_player_state(self.side).position
        my_trail = state.get_player_state(self.side).trail

        queue = deque([(my_pos, [])])
        visited = {my_pos}

        directions = {
            Action.UP: (0, -1),
            Action.DOWN: (0, 1),
            Action.LEFT: (-1, 0),
            Action.RIGHT: (1, 0)
        }
        
        ex, ey = enemy_pos
        danger_zone = {(ex+1, ey), (ex-1, ey), (ex, ey+1), (ex, ey-1)}

        while queue:
            curr_pos, path = queue.popleft()

            if curr_pos in targets and path:
                return path[0]

            for action, (dx, dy) in directions.items():
                nx, ny = curr_pos[0] + dx, curr_pos[1] + dy
                next_pos = (nx, ny)

                if nx < 0 or nx >= board.width or ny < 0 or ny >= board.height:
                    continue

                if next_pos in board.walls or next_pos in my_trail:
                    continue

                if next_pos in danger_zone and next_pos != enemy_pos and next_pos not in enemy_trail:
                    continue

                if next_pos not in visited:
                    visited.add(next_pos)
                    queue.append((next_pos, path + [action]))

        return None
    
    def dynamic_a_star(self, state: GameState, targets: set, enemy_pos: tuple, enemy_trail: set) -> Action | None:
        if not targets:
            return None

        board = state.board
        my_pos = state.get_player_state(self.side).position
        my_trail = state.get_player_state(self.side).trail

        pq = []
        tie_breaker = itertools.count()
        best_cost = {my_pos: 0}

        if targets:
            anchor_target = min(
                targets, 
                key=lambda t: abs(my_pos[0] - t[0]) + abs(my_pos[1] - t[1])
            )
        else:
            return None

        # one of the most exact admissible heuristic function:
        def get_heuristic(pos: tuple) -> int:
            return abs(pos[0] - anchor_target[0]) + abs(pos[1] - anchor_target[1])

        # # one of the most exact admissible heuristic function:
        # def get_heuristic(pos: tuple) -> int:
        #     return min(abs(pos[0] - tx) + abs(pos[1] - ty) for tx, ty in targets)

        initial_h = get_heuristic(my_pos)
        heapq.heappush(pq, (initial_h, next(tie_breaker), 0, my_pos, []))

        directions = {
            Action.UP: (0, -1),
            Action.DOWN: (0, 1),
            Action.LEFT: (-1, 0),
            Action.RIGHT: (1, 0)
        }
        
        ex, ey = enemy_pos
        danger_zone = {(ex+1, ey), (ex-1, ey), (ex, ey+1), (ex, ey-1)}

        while pq:
            f_score, _, g_score, curr_pos, path = heapq.heappop(pq)

            if curr_pos in targets and path:
                return path[0]

            if g_score > best_cost.get(curr_pos, float('inf')):
                continue

            for action, (dx, dy) in directions.items():
                nx, ny = curr_pos[0] + dx, curr_pos[1] + dy
                next_pos = (nx, ny)

                if nx < 0 or nx >= board.width or ny < 0 or ny >= board.height:
                    continue

                if next_pos in board.walls or next_pos in my_trail:
                    continue

                if next_pos in danger_zone and next_pos != enemy_pos and next_pos not in enemy_trail:
                    continue

                new_cost = g_score + 1
                
                if next_pos not in best_cost or new_cost < best_cost[next_pos]:
                    best_cost[next_pos] = new_cost
                    priority = new_cost + get_heuristic(next_pos)
                    heapq.heappush(pq, (priority, next(tie_breaker), new_cost, next_pos, path + [action]))

        return None

    def get_safe_fallback_move(self, state: GameState, enemy_pos: tuple, enemy_trail: set) -> Action:
        board = state.board
        my_pos = state.get_player_state(self.side).position
        my_trail = state.get_player_state(self.side).trail

        directions = {
            Action.UP: (0, -1),
            Action.DOWN: (0, 1),
            Action.LEFT: (-1, 0),
            Action.RIGHT: (1, 0)
        }
        
        ex, ey = enemy_pos
        danger_zone = {(ex+1, ey), (ex-1, ey), (ex, ey+1), (ex, ey-1)}

        for action, (dx, dy) in directions.items():
            nx, ny = my_pos[0] + dx, my_pos[1] + dy
            next_pos = (nx, ny)

            if 0 <= nx < board.width and 0 <= ny < board.height:
                if next_pos not in board.walls and next_pos not in my_trail:
                    if next_pos in danger_zone and next_pos != enemy_pos and next_pos not in enemy_trail:
                        continue
                    return action
                    
        return Action.STAY