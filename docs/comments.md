<!--
========================================================================================================================

    This is a Markdown file. If you are using VS Code, right-click this file and click "Open Preview" to render it!
    
========================================================================================================================
-->

# Comments

| [`Action`](#action) | [`Board`](#board) | [`GameState`](#gamestate) | [`Player`](#player) | [`PlayerState`](#playerstate) | [`Tile`](#tile) |
| :---: | :---: | :---: | :---: | :---: | :---: |

<br>

This file contains doc comments for the classes defined in `segmentation_core.engine`.

### `Action`

```python
class Action:
    r"""
    Represents a player action.
    """

    UP: Action = ...
    DOWN: Action = ...
    LEFT: Action = ...
    RIGHT: Action = ...
    STAY: Action = ...
```

### `Board`

```python
class Board:
    r"""
    Represents the state of the board.
    Stores the dimensions, board layout, and state of each tile.
    """
    
    @property
    def width(self) -> int:
        r"""
        Returns the width of the board.
        """

    @property
    def height(self) -> int:
        r"""
        Returns the height of the board.
        """

    @property
    def walls(self) -> set:
        r"""
        Returns the walls of the board as a set of (x, y) tuples.
        """

    def get_tile(self, x:int, y:int) -> Tile | None:
        r"""
        Returns the tile at the given (x, y) position, or None if out of bounds.

        Parameters:
           - `x` (`int`): The x-coordinate (column index) of the tile on the board.
           - `y` (`int`): The y-coordinate (row index) of the tile on the board.

        Returns:
           - `Tile`: The tile at the given position, if within bounds.
           - `None`: If the position is out of bounds.
        """

    def clone(self) -> Board:
        r"""
        Returns a clone of the board.
        """
```

### `GameState`

```python
class GameState:
    r"""
    Represents the entire game state and holds the bulk of the game logic.
    The board is initialized from a file containing the dimensions,
    board layout, and starting positions of each player.
    """
    
    @property
    def board(self) -> Board:
        r"""
        The board associated with the game state.
        """

    @property
    def player_one(self) -> PlayerState:
        r"""
        The state of Player 1.
        """

    @property
    def player_two(self) -> PlayerState:
        r"""
        The state of Player 2.
        """

    @property
    def active_player(self) -> Player:
        r"""
        The player whose turn it is.
        """

    @property
    def winner(self) -> Player | None:
        r"""
        The player who has won the game, if there is one. Otherwise, None
        """

    def get_player_state(self, player:Player) -> PlayerState:
        r"""
        Returns the state of the specified player.

        Parameters:
           - `player`: The player whose state is to be retrieved.

        Returns:
           - `PlayerState`: The state of the specified player.
        """

    def transition(self, action:Action) -> GameState:
        r"""
        Transitions the board state based on the action taken by the active player. This
        function DOES NOT mutate the current board state in-place.

        A player can take one of five actions: Up, Down, Left, Right, or Stay. `GameState`s that are
        already in a terminal state (i.e. have a winner) will not be changed.

        Attempting to move into a wall or out-of-bounds will result in the player staying in place and the turn
        to be passed to the other player.

        Otherwise, game checks are performed in the following order:
            1.  If the active player moves onto the tile that the other player is on, the active player wins.
            2.  If the active player moves onto a tile that is part of a trail, the trail's owner loses.
            3.  (a) If the active player moves onto a tile that they have claimed, the area enclosed by their
                trail and claim is filled as their claim. If the other player is in this area, the other
                player loses.
        .        (b) Otherwise, the active player's trail is extended to include their new position.
            4. If the active player has claimed more than half of the board, they win.

         Following these checks, the player's position is updated, and the turn is passed to the other player.

         Parameters:
            - `action` (`Action`): The action taken by the active player.

         Returns:
            - `GameState`: A new `GameState` instance representing the state of the game after the action has been applied.
        """

    def clone(self) -> GameState:
        r"""
        Returns a clone of the game state.
        """
```

### `Player`

```python
class Player:
    r"""
    Represents one of the two players.
    """
    
    PLAYER_ONE: Player = ...
    PLAYER_TWO: Player = ...

    def other(self) -> Player:
        r"""
        Gets the opposing player of the current player.

        Returns:
           - `Player.PLAYER_ONE`: If the current player is Player.PLAYER_TWO.
           - `Player.PLAYER_TWO`: If the current player is Player.PLAYER_ONE.
        """
```

### `PlayerState`

```python
class PlayerState:
    r"""
    Represents the state of a player, including its position, claims, and trail.
    """
    
    @property
    def player(self) -> Player:
        r"""
        The player this state belongs to.
        """

    @property
    def position(self) -> tuple:
        r"""
        The current position of the player.
        """

    @property
    def claims(self) -> set:
        r"""
        The cells claimed by the player as a set of (x, y) tuples.
        """

    @property
    def trail(self) -> set:
        r"""
        The current trail of the player as a set of (x, y) tuples.
        """

    def clone(self) -> PlayerState:
        r"""
        Returns a clone of the player state.
        """
```

### `Tile`

```python
class Tile:
    r"""
    Represents the state of a tile on the board.
    If a tile is not a wall, it can either be empty or contain one or more of a player's trail, a player's claim, and a player themself.
    """
    
    def is_wall(self) -> bool:
        r"""
        Checks if the tile is a wall.
        """

    def trail(self) -> Player | None:
        r"""
        Returns the player who owns the trail on the tile, if there is one.
        Otherwise, returns None.

        Returns:
          - `Player` if there is a trail owned by the player.
          - `None`   if there is no trail.
        """

    def claim(self) -> Player | None:
        r"""
        Returns the player who owns the claim on the tile, if there is one.
        Otherwise, returns None.

        Returns:
         - `Player` if there is a claim owned by the player.
         - `None`   if there is no claim.
        """

    def player(self) -> Player | None:
        r"""
        Returns the player who owns the player on the tile, if there is one.
        Otherwise, returns None.

        Returns:
        - `Player` if there is a player owned by the player.
        - `None`   if there is no player.
        """

    def clone(self) -> Tile:
        r"""
        Returns a clone of the tile.
        """
```

<br>

---

| [`Back to top`](#comments) |
| :---: |
