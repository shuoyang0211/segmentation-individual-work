import pygame

from segmentation_core.engine import GameState, Player

_SCREEN = None
_FONT = None
_TILE = 40            # px per tile
_SIDEBAR = 220        # px for labels
_INITED = False

WHITE   = (255, 255, 255)
BG      = (245, 246, 250)
GRID    = (210, 214, 220)
RED     = (230, 57, 70)
DARK_RED = (180, 30, 50)  # player 1
BLUE    = (66, 135, 245)
DARK_BLUE = (30, 90, 200) # player 2
BLACK   = (30, 30, 30)
GOLD    = (255, 215, 0)

def _ensure_pygame(width: int, height: int):
    global _SCREEN, _FONT, _INITED
    if _INITED:
        return
    pygame.init()
    pygame.display.set_caption("Segmentation – Board")
    win_w = width * _TILE + _SIDEBAR
    win_h = height * _TILE
    _SCREEN = pygame.display.set_mode((win_w, win_h))
    _FONT = pygame.font.SysFont(None, 28)
    _INITED = True

def _cell_rect(x: int, y: int) -> pygame.Rect:
    return pygame.Rect(x * _TILE, y * _TILE, _TILE, _TILE)

def _draw_grid(board_w: int, board_h: int):
    assert _INITED and _SCREEN is not None and _FONT is not None

    # background
    _SCREEN.fill(BG)
    # cells
    for y in range(board_h):
        for x in range(board_w):
            r = _cell_rect(x, y)
            pygame.draw.rect(_SCREEN, WHITE, r)
            pygame.draw.rect(_SCREEN, GRID, r, 1)

def _draw_players(p1_pos, p2_pos):
    assert _INITED and _SCREEN is not None and _FONT is not None

    pad = 6  # inset so squares don’t touch grid lines
    # Player 1 (red)
    rx, ry = p1_pos
    rr = _cell_rect(rx, ry).inflate(-2*pad, -2*pad)
    pygame.draw.rect(_SCREEN, DARK_RED, rr)
    # Player 2 (blue)
    bx, by = p2_pos
    br = _cell_rect(bx, by).inflate(-2*pad, -2*pad)
    pygame.draw.rect(_SCREEN, DARK_BLUE, br)

def _draw_claims(p1_claims, p2_claims):
    assert _INITED and _SCREEN is not None and _FONT is not None

    pad = 6  # inset so squares don’t touch grid lines
    for (x, y) in p1_claims:
        r = _cell_rect(x, y).inflate(-2*pad, -2*pad)
        pygame.draw.rect(_SCREEN, RED, r)
    for (x, y) in p2_claims:
        r = _cell_rect(x, y).inflate(-2*pad, -2*pad)
        pygame.draw.rect(_SCREEN, BLUE, r)

def _draw_trails(p1_trail, p2_trail):
    assert _INITED and _SCREEN is not None and _FONT is not None

    pad = 10  # inset so squares don’t touch grid lines
    for (x, y) in p1_trail:
        r = _cell_rect(x, y).inflate(-2*pad, -2*pad)
        pygame.draw.circle(_SCREEN, RED, r.center, r.width // 2)
    for (x, y) in p2_trail:
        r = _cell_rect(x, y).inflate(-2*pad, -2*pad)
        pygame.draw.circle(_SCREEN, BLUE, r.center, r.width // 2)

def _draw_walls(walls):
    assert _INITED and _SCREEN is not None and _FONT is not None

    pad = 6  # inset so squares don’t touch grid lines
    for (x, y) in walls:
        r = _cell_rect(x, y).inflate(-2*pad, -2*pad)
        pygame.draw.rect(_SCREEN, BLACK, r)

def _draw_sidebar(game_state: GameState):
    assert _INITED and _SCREEN is not None and _FONT is not None

    board_w = game_state.board.width
    win_left = board_w * _TILE
    x = win_left + 14
    y = 16

    # Title
    title = _FONT.render("Score", True, BLACK)
    _SCREEN.blit(title, (x, y))
    y += 12 + title.get_height()

    # Counts
    p1_claim = len(game_state.player_one.claims)
    p2_claim = len(game_state.player_two.claims)

    p1_surf = _FONT.render(f"Player 1: {p1_claim}", True, RED)
    p2_surf = _FONT.render(f"Player 2: {p2_claim}", True, BLUE)

    _SCREEN.blit(p1_surf, (x + 24, y))
    y2 = y + p1_surf.get_height() + 10
    _SCREEN.blit(p2_surf, (x + 24, y2))

    # Active turn star
    is_p1_turn = (game_state.active_player == Player.PLAYER_ONE)
    star = _FONT.render("★", True, GOLD)
    if is_p1_turn:
        _SCREEN.blit(star, (x, y))
    else:
        _SCREEN.blit(star, (x, y2))



def render(game_state: GameState):
    board_w = game_state.board.width
    board_h = game_state.board.height
    _ensure_pygame(board_w, board_h)

    # Keep window responsive / allow close
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    # Draw
    _draw_grid(board_w, board_h)
    _draw_claims(
        game_state.player_one.claims,
        game_state.player_two.claims,
    )
    _draw_trails(
        game_state.player_one.trail,
        game_state.player_two.trail,
    )
    _draw_players(
        game_state.player_one.position,
        game_state.player_two.position,
    )
    _draw_walls(game_state.board.walls)
    _draw_sidebar(game_state)

    pygame.display.flip()