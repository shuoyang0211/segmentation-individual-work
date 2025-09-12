import pygame
import pygame.freetype as ft

from segmentation_core.engine import GameState, Player


class Renderer:
    DEFAULT_MIN_W = 1024
    DEFAULT_MIN_H = 720
    MIN_CELL_PX = 8
    MAX_CELL_PX = 128

    HUD_H = 72
    HUD_MARGIN = 16
    CARD_GAP = 16
    CARD_PAD_X = 12
    CARD_PAD_Y = 12
    NAME_SCORE_GAP = -4
    CARD_MIN_W = 220
    CARD_MAX_W = 340
    STRIP_W = 6
    SWATCH_SIZE = 28
    SWATCH_GAP = 14

    GRID_TOP_PAD = 16
    GRID_BOTTOM_PAD = 16

    TURN_PAD_X = 10
    TURN_PAD_Y = 6
    TURN_BG = (60, 55, 30)

    BG = (30, 30, 36)
    PANEL_BG = (18, 18, 22)
    TEXT = (230, 230, 235)

    GRID = (60, 60, 72)
    GRID_5 = (110, 110, 130)
    GRID_10 = (160, 160, 180)

    TILE_BG = (40, 40, 48)
    WALL = (90, 90, 90)

    P1 = (220, 90, 70)
    P2 = (70, 120, 220)

    P1_DARK = (140, 20, 10)
    P2_DARK = (20, 60, 140)

    CLAIM_A = (220, 90, 70, 80)
    CLAIM_B = (70, 120, 220, 80)

    GOLD = (255, 215, 0)

    def __init__(
        self,
        initial_board_size: tuple[int, int] = (20, 15),
        window_title: str = "Segmentation",
    ) -> None:
        if not pygame.get_init():
            pygame.init()
        pygame.display.set_caption(window_title)

        self._board_w0, self._board_h0 = initial_board_size

        self._tile: int = self._auto_cell_size(self._board_w0, self._board_h0)
        self._screen: pygame.Surface = self._create_fitted_window(
            self._board_w0, self._board_h0
        )

        self._font: ft.Font = ft.Font(None, 24)
        self._font_small: ft.Font = ft.Font(None, 18)

        self._last_board_size: tuple[int, int] = (self._board_w0, self._board_h0)

    def _desktop_size(self) -> tuple[int, int]:
        info = pygame.display.Info()
        return info.current_w, info.current_h

    def _auto_cell_size(self, board_w: int, board_h: int) -> int:
        desk_w, desk_h = self._desktop_size()
        avail_w = int(desk_w * 0.90)
        avail_h = int(desk_h * 0.90) - (
            self.HUD_H + self.GRID_TOP_PAD + self.GRID_BOTTOM_PAD
        )
        cell_w = avail_w // max(1, board_w)
        cell_h = avail_h // max(1, board_h)
        return max(self.MIN_CELL_PX, min(self.MAX_CELL_PX, min(cell_w, cell_h)))

    def _create_fitted_window(self, board_w: int, board_h: int) -> pygame.Surface:
        desk_w, desk_h = self._desktop_size()
        max_w = int(desk_w * 0.98)
        max_h = int(desk_h * 0.98)
        win_w = min(max(self.DEFAULT_MIN_W, board_w * self._tile), max_w)
        win_h = min(
            max(
                self.DEFAULT_MIN_H,
                self.HUD_H
                + self.GRID_TOP_PAD
                + board_h * self._tile
                + self.GRID_BOTTOM_PAD,
            ),
            max_h,
        )
        return pygame.display.set_mode((win_w, win_h), pygame.RESIZABLE)

    def _board_origin(self, board_w: int, board_h: int) -> tuple[int, int]:
        win_w, win_h = self._screen.get_size()
        grid_w = board_w * self._tile
        grid_h = board_h * self._tile
        x = (win_w - grid_w) // 2
        avail_h = win_h - self.HUD_H - self.GRID_TOP_PAD - self.GRID_BOTTOM_PAD
        y = self.HUD_H + self.GRID_TOP_PAD + max(0, (avail_h - grid_h) // 2)
        return max(0, x), max(self.HUD_H + self.GRID_TOP_PAD, y)

    def _cell_rect(self, x: int, y: int, board_w: int, board_h: int) -> pygame.Rect:
        ox, oy = self._board_origin(board_w, board_h)
        return pygame.Rect(
            ox + x * self._tile, oy + y * self._tile, self._tile, self._tile
        )

    def _render_text(self, font: ft.Font, text: str, color) -> pygame.Surface:
        surf, _ = font.render(text, color)
        return surf

    def _ellipsize(
        self, font: ft.Font, text: str, max_w: int, color=TEXT
    ) -> pygame.Surface:
        if max_w <= 0:
            surf, _ = font.render("…", color)
            return surf
        surf, _ = font.render(text, color)
        if surf.get_width() <= max_w:
            return surf
        base = text
        ell = "…"
        while base and font.render(base + ell, color)[0].get_width() > max_w:
            base = base[:-1]
        return font.render((base + ell) if base else ell, color)[0]

    def _max_tile_that_fits(self, board_w: int, board_h: int) -> int:
        win_w, win_h = self._screen.get_size()
        avail_w = win_w
        avail_h = win_h - self.HUD_H - self.GRID_TOP_PAD - self.GRID_BOTTOM_PAD
        if board_w <= 0 or board_h <= 0:
            return self._tile
        t_w = avail_w // board_w
        t_h = avail_h // board_h
        t = min(t_w, t_h)
        return max(self.MIN_CELL_PX, min(self.MAX_CELL_PX, t))

    def _ensure_grid_fits(self, board_w: int, board_h: int) -> None:
        fit = self._max_tile_that_fits(board_w, board_h)
        if self._tile > fit:
            self._tile = fit

    def _draw_grid(self, board_w: int, board_h: int) -> None:
        self._screen.fill(self.BG)
        ox, oy = self._board_origin(board_w, board_h)

        for y in range(board_h):
            for x in range(board_w):
                r = pygame.Rect(
                    ox + x * self._tile, oy + y * self._tile, self._tile, self._tile
                )
                pygame.draw.rect(self._screen, self.TILE_BG, r)

        gw = board_w * self._tile
        gh = board_h * self._tile
        for r in range(board_h + 1):
            y = oy + r * self._tile
            if r % 10 == 0:
                col, w = self.GRID_10, 3 if self._tile >= 24 else 2
            elif r % 5 == 0:
                col, w = self.GRID_5, 2 if self._tile >= 20 else 1
            else:
                col, w = self.GRID, 1
            pygame.draw.line(self._screen, col, (ox, y), (ox + gw, y), w)

        for c in range(board_w + 1):
            x = ox + c * self._tile
            if c % 10 == 0:
                col, w = self.GRID_10, 3 if self._tile >= 24 else 2
            elif c % 5 == 0:
                col, w = self.GRID_5, 2 if self._tile >= 20 else 1
            else:
                col, w = self.GRID, 1
            pygame.draw.line(self._screen, col, (x, oy), (x, oy + gh), w)

    def _draw_players(self, p1_pos, p2_pos, board_w: int, board_h: int) -> None:
        pad = max(4, self._tile // 6)
        rx, ry = p1_pos
        rr = self._cell_rect(rx, ry, board_w, board_h).inflate(-2 * pad, -2 * pad)
        rr_outline = rr.inflate(2, 2)
        pygame.draw.rect(self._screen, (255, 255, 255), rr_outline, border_radius=6)
        pygame.draw.rect(self._screen, self.P1_DARK, rr, border_radius=6)

        bx, by = p2_pos
        br = self._cell_rect(bx, by, board_w, board_h).inflate(-2 * pad, -2 * pad)
        br_outline = br.inflate(2, 2)
        pygame.draw.rect(self._screen, (255, 255, 255), br_outline, border_radius=6)
        pygame.draw.rect(self._screen, self.P2_DARK, br, border_radius=6)

    def _draw_claims(self, p1_claims, p2_claims, board_w: int, board_h: int) -> None:
        for x, y in p1_claims:
            r = self._cell_rect(x, y, board_w, board_h)
            s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill(self.CLAIM_A)
            self._screen.blit(s, r.topleft)
        for x, y in p2_claims:
            r = self._cell_rect(x, y, board_w, board_h)
            s = pygame.Surface((r.w, r.h), pygame.SRCALPHA)
            s.fill(self.CLAIM_B)
            self._screen.blit(s, r.topleft)

    def _draw_trails(self, p1_trail, p2_trail, board_w: int, board_h: int) -> None:
        radius = max(4, int(self._tile * 0.33))
        for x, y in p1_trail:
            r = self._cell_rect(x, y, board_w, board_h)
            pygame.draw.circle(self._screen, self.P1, r.center, radius)
        for x, y in p2_trail:
            r = self._cell_rect(x, y, board_w, board_h)
            pygame.draw.circle(self._screen, self.P2, r.center, radius)

    def _draw_walls(self, walls, board_w: int, board_h: int) -> None:
        pad = max(4, self._tile // 6)
        for x, y in walls:
            r = self._cell_rect(x, y, board_w, board_h).inflate(-2 * pad, -2 * pad)
            pygame.draw.rect(self._screen, self.WALL, r, border_radius=4)

    def _draw_hud(self, game_state: GameState) -> None:
        hud_rect = pygame.Rect(0, 0, self._screen.get_width(), self.HUD_H)
        pygame.draw.rect(self._screen, self.PANEL_BG, hud_rect)

        p1_score = len(game_state.player_one.claims)
        p2_score = len(game_state.player_two.claims)
        turn_p1 = game_state.active_player == Player.PLAYER_ONE

        avail_w = hud_rect.w - 2 * self.HUD_MARGIN
        two_col_target = min(self.CARD_MAX_W, (avail_w - self.CARD_GAP) // 2)
        two_col_ok = two_col_target >= self.CARD_MIN_W

        name_h = self._font.get_sized_height(24)
        score_h = self._font.get_sized_height(24)
        chip_h = self._font_small.get_sized_height(18) + 2 * self.TURN_PAD_Y
        content_min_h = max(
            self.SWATCH_SIZE + 2 * self.CARD_PAD_Y,
            (
                self.CARD_PAD_Y
                + name_h
                + self.NAME_SCORE_GAP
                + score_h
                + self.CARD_PAD_Y
            ),
            chip_h + 2 * self.CARD_PAD_Y,
        )

        if two_col_ok:
            card_w = two_col_target
            card_h = max(content_min_h, self.HUD_H - 18)
            y = (hud_rect.h - card_h) // 2
            left_rect = pygame.Rect(self.HUD_MARGIN, y, card_w, card_h)
            right_rect = pygame.Rect(
                hud_rect.right - self.HUD_MARGIN - card_w, y, card_w, card_h
            )
            rows_stacked = False
        else:
            card_w = max(self.CARD_MIN_W, min(self.CARD_MAX_W, avail_w))
            card_h = max(content_min_h, self.HUD_H // 2 - 8)
            top_y = (hud_rect.h - (card_h * 2 + self.CARD_GAP)) // 2
            left_rect = pygame.Rect((hud_rect.w - card_w) // 2, top_y, card_w, card_h)
            right_rect = pygame.Rect(
                left_rect.x, left_rect.bottom + self.CARD_GAP, card_w, card_h
            )
            rows_stacked = True

        def draw_card(
            rect: pygame.Rect,
            color,
            name: str,
            score: str,
            active: bool,
            align_left: bool,
        ):
            bg = (45, 45, 55) if not active else (90, 90, 110)
            pygame.draw.rect(self._screen, bg, rect, border_radius=12)

            strip = (
                pygame.Rect(rect.left, rect.top, self.STRIP_W, rect.h)
                if align_left
                else pygame.Rect(
                    rect.right - self.STRIP_W, rect.top, self.STRIP_W, rect.h
                )
            )
            pygame.draw.rect(self._screen, color, strip, border_radius=6)

            sw = pygame.Rect(0, 0, self.SWATCH_SIZE, self.SWATCH_SIZE)
            sw.centery = rect.centery
            if align_left:
                sw.left = rect.left + self.STRIP_W + self.CARD_PAD_X
            else:
                sw.right = rect.right - self.STRIP_W - self.CARD_PAD_X
            pygame.draw.rect(self._screen, color, sw, border_radius=6)

            chip_w = chip_h = 0
            chip_surf = None
            if active:
                chip_text = "YOUR TURN"
                chip_surf, _ = self._font_small.render(chip_text, self.GOLD)
                chip_w = chip_surf.get_width() + 2 * self.TURN_PAD_X
                chip_h = chip_surf.get_height() + 2 * self.TURN_PAD_Y

            if align_left:
                text_x = sw.right + self.SWATCH_GAP
                chip_reserve_right = (self.CARD_PAD_X + chip_w) if active else 0
                max_text_right = (
                    rect.right - self.STRIP_W - chip_reserve_right - self.CARD_PAD_X
                )
                max_w = max(0, max_text_right - text_x)
            else:
                chip_reserve_left = (self.CARD_PAD_X + chip_w) if active else 0
                max_text_left = (
                    rect.left + self.STRIP_W + chip_reserve_left + self.CARD_PAD_X
                )
                max_w = max(0, (sw.left - self.SWATCH_GAP) - max_text_left)

            name_s = self._ellipsize(self._font, name, max_w, self.TEXT)
            score_s = self._ellipsize(self._font, score, max_w, self.TEXT)

            name_y = rect.top + self.CARD_PAD_Y
            score_y = rect.bottom - self.CARD_PAD_Y - score_s.get_height()

            if align_left:
                self._screen.blit(name_s, (text_x, name_y))  # type: ignore
                self._screen.blit(score_s, (text_x, score_y))  # type: ignore
                if active and chip_surf is not None:
                    chip_rect = pygame.Rect(0, 0, chip_w, chip_h)
                    chip_rect.top = rect.top + self.CARD_PAD_Y - 2
                    chip_rect.right = rect.right - self.STRIP_W - self.CARD_PAD_X
                    pygame.draw.rect(
                        self._screen, self.TURN_BG, chip_rect, border_radius=8
                    )
                    chip_pos = (
                        chip_rect.left + self.TURN_PAD_X,
                        chip_rect.top + self.TURN_PAD_Y,
                    )
                    self._screen.blit(chip_surf, chip_pos)
            else:
                name_x = (sw.left - self.SWATCH_GAP) - name_s.get_width()
                score_x = (sw.left - self.SWATCH_GAP) - score_s.get_width()
                min_x = (
                    rect.left
                    + self.STRIP_W
                    + self.CARD_PAD_X
                    + (chip_w + self.CARD_PAD_X if active else 0)
                )
                name_x = max(name_x, min_x)
                score_x = max(score_x, min_x)
                self._screen.blit(name_s, (name_x, name_y))
                self._screen.blit(score_s, (score_x, score_y))
                if active and chip_surf is not None:
                    chip_rect = pygame.Rect(0, 0, chip_w, chip_h)
                    chip_rect.top = rect.top + self.CARD_PAD_Y - 2
                    chip_rect.left = rect.left + self.STRIP_W + self.CARD_PAD_X
                    pygame.draw.rect(
                        self._screen, self.TURN_BG, chip_rect, border_radius=8
                    )
                    chip_pos = (
                        chip_rect.left + self.TURN_PAD_X,
                        chip_rect.top + self.TURN_PAD_Y,
                    )
                    self._screen.blit(chip_surf, chip_pos)

        draw_card(
            left_rect, self.P1, "Player 1", str(p1_score), turn_p1, align_left=True
        )
        draw_card(
            right_rect,
            self.P2,
            "Player 2",
            str(p2_score),
            not turn_p1,
            align_left=(False if not rows_stacked else True),
        )

    def _draw_winner_popup(self, game_state: GameState) -> None:
        winner = game_state.winner
        if not winner:
            return
        overlay = pygame.Surface(self._screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self._screen.blit(overlay, (0, 0))
        if winner == Player.PLAYER_ONE:
            color = self.P1
            title = "Player 1 Wins!"
        else:  # winner == Player.PLAYER_TWO
            color = self.P2
            title = "Player 2 Wins!"
        p1_score = len(game_state.player_one.claims)
        p2_score = len(game_state.player_two.claims)
        big_font = ft.Font(None, 48)
        mid_font = ft.Font(None, 28)
        title_surf, _ = big_font.render(title, self.TEXT)
        score_text = f"{p1_score} - {p2_score}"
        score_surf, _ = mid_font.render(score_text, self.TEXT)
        pad_x = 28
        pad_y = 22
        gap = 12
        box_w = max(title_surf.get_width(), score_surf.get_width()) + 2 * pad_x
        box_h = title_surf.get_height() + gap + score_surf.get_height() + 2 * pad_y
        win_w, win_h = self._screen.get_size()
        box = pygame.Rect((win_w - box_w) // 2, (win_h - box_h) // 2, box_w, box_h)
        pygame.draw.rect(self._screen, (45, 45, 55), box, border_radius=14)
        strip = pygame.Rect(box.left, box.top, box.w, 6)
        pygame.draw.rect(self._screen, color, strip, border_radius=3)
        self._screen.blit(
            title_surf, (box.centerx - title_surf.get_width() // 2, box.top + pad_y)
        )
        self._screen.blit(
            score_surf,
            (
                box.centerx - score_surf.get_width() // 2,
                box.bottom - pad_y - score_surf.get_height(),
            ),
        )

    def _handle_events(self, board_w: int, board_h: int):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.VIDEORESIZE:
                desk_w, desk_h = self._desktop_size()
                new_w = min(max(event.w, self.DEFAULT_MIN_W), int(desk_w * 0.98))
                new_h = min(max(event.h, self.DEFAULT_MIN_H), int(desk_h * 0.98))
                self._screen = pygame.display.set_mode((new_w, new_h), pygame.RESIZABLE)
                self._ensure_grid_fits(board_w, board_h)
                self._tile = self._max_tile_that_fits(board_w, board_h)

    def render(self, game_state: GameState):
        board_w = game_state.board.width
        board_h = game_state.board.height

        if (board_w, board_h) != self._last_board_size:
            self._screen = self._create_fitted_window(board_w, board_h)
            self._last_board_size = (board_w, board_h)

        self._handle_events(board_w, board_h)
        self._ensure_grid_fits(board_w, board_h)

        self._draw_grid(board_w, board_h)
        self._draw_claims(
            game_state.player_one.claims, game_state.player_two.claims, board_w, board_h
        )
        self._draw_trails(
            game_state.player_one.trail, game_state.player_two.trail, board_w, board_h
        )
        self._draw_players(
            game_state.player_one.position,
            game_state.player_two.position,
            board_w,
            board_h,
        )
        self._draw_walls(game_state.board.walls, board_w, board_h)
        self._draw_hud(game_state)
        self._draw_winner_popup(game_state)

        pygame.display.flip()
