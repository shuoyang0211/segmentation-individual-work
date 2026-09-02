<!--
========================================================================================================================

    This is a Markdown file. If you're using VS Code, right-click the filename and select "Open Preview" to render it!

========================================================================================================================
-->

# Comments

| [`GameState`](#gamestate) | [`Player`](#player) | [`PlayerState`](#playerstate) | [`Board`](#board) | [`Tile`](#tile) | [`Action`](#action) |
| :---: | :---: | :---: | :---: | :---: | :---: |

<br>

This file contains documentation for the classes defined in `segmentation_core.engine`.

## `GameState`

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
        Returns the board associated with the game state.
        """

    @property
    def player_one(self) -> PlayerState:
        r"""
        Returns the state state of player one.
        """

    @property
    def player_two(self) -> PlayerState:
        r"""
        Returns the state state of player two.
        """

    @property
    def active_player(self) -> Player:
        r"""
        Returns the player to move.
        """

    @property
    def winner(self) -> Player | None:
        r"""
        Returns the winner of the game, if there is one.
        """

    def get_player_state(self, player: Player) -> PlayerState:
        r"""
        Returns the state of the specified player.
        """

    def transition(self, action: Action) -> GameState:
        r"""
        Returns the game state that would result from the current player taking
        the given action. Note that this does not mutate the current game state.
        """

    def clone(self) -> GameState:
        r"""
        Returns a clone of the game state.
        """
```

## `Player`

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
        """
```

## `PlayerState`

```python
class PlayerState:
    r"""
    Represents the state of a player, including its position, claims, and trail.
    """

    @property
    def player(self) -> Player:
        r"""
        Returns the player to which this state belongs.
        """

    @property
    def position(self) -> tuple:
        r"""
        Returns the current position of the player.
        """

    @property
    def claims(self) -> set(tuple[int, int]):
        r"""
        Returns the set of positions claimed by the player.
        """

    @property
    def trail(self) -> set(tuple[int, int]):
        r"""
        Returns the player's current trail as a set of positions.
        """

    def clone(self) -> PlayerState:
        r"""
        Returns a clone of the player state.
        """
```

## `Board`

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

    def get_tile(self, x: int, y: int) -> Tile | None:
        r"""
        Returns the tile at position (x, y), or None if out of bounds.
        """

    def clone(self) -> Board:
        r"""
        Returns a clone of the board.
        """
```

## `Tile`

```python
class Tile:
    r"""
    Represents the state of a tile on the board.
    If a tile is not a wall, it can either be empty or contain one or more of
    a player's trail, a player's claim, and a player themself.
    """

    def is_wall(self) -> bool:
        r"""
        Returns True if the tile is a wall.
        """

    def trail(self) -> Player | None:
        r"""
        Returns the player who owns a trail on this tile, if there is one.
        """

    def claim(self) -> Player | None:
        r"""
        Returns the player who owns a claim on this tile, if there is one.
        """

    def player(self) -> Player | None:
        r"""
        Returns the player currently on this tile, if there is one.
        """

    def clone(self) -> Tile:
        r"""
        Returns a clone of the tile.
        """
```

## `Action`

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

<br>

---

| [`Back to top`](#comments) |
| :---: |
