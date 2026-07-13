"""
Usage examples:
    # Edit an existing board file
    python board_editor.py --load maps/level1.board

    # Create a new blank board (20x15) and save to a path when pressing 'S'
    python board_editor.py --size 20x15 --out maps/new_level.board

    # Create a new board with a different cell size
    python board_editor.py --size 30x18 --cell 28

Controls:
    Mouse:
      - Left-click / drag: paint with selected tool
      - Right-click: erase to Empty (E)
      - Mouse wheel: scroll (Shift + wheel for horizontal)
      - Drag scrollbar thumbs to scroll
    Tools (select with keyboard):
      - 1 or A: place Player 1 (A)  [only one on the board]
      - 2 or B: place Player 2 (B)  [only one on the board]
      - W: place Wall (W)
      - E: place Empty (E)
    Other:
      - S: save (to --out if provided; otherwise to --load path or default name)
      - G: toggle grid lines
      - +/-: zoom cell size (16..128)
      - H: toggle help overlay
      - Esc: quit
"""

from __future__ import annotations

import argparse
import re
from typing import List, Tuple, Optional

import pygame
import pygame.freetype as ft


TOKEN_RE = re.compile(r"([A-Z])(\d+)")
ALLOWED_TILES = {"E", "W", "A", "B"}


def parse_dimensions(dim: str) -> Tuple[int, int]:
    dim = dim.strip().lower().replace(" ", "")
    if "x" not in dim:
        raise ValueError("Invalid dimensions format, expected WIDTHxHEIGHT")
    w_str, h_str = dim.split("x", 1)
    w = int(w_str)
    h = int(h_str)
    if w <= 0 or h <= 0:
        raise ValueError("Dimensions must be positive")
    return w, h


def rle_decode_row(line: str, width: int, row_idx: int) -> List[str]:
    tiles: List[str] = []
    pos = 0
    for m in TOKEN_RE.finditer(line.strip()):
        t, n_str = m.groups()
        if t not in ALLOWED_TILES:
            raise ValueError(f"Unknown tile '{t}' on row {row_idx + 1}")
        n = int(n_str)
        if t in ("A", "B") and n != 1:
            raise ValueError(f"Player tile '{t}' count must be 1 on row {row_idx + 1}")
        tiles.extend([t] * n)
        pos = m.end()
    if pos != len(line.strip()):
        raise ValueError(
            f"Invalid token(s) on row {row_idx + 1}: '{line[pos:].strip()}'"
        )
    if len(tiles) != width:
        raise ValueError(
            f"Width mismatch on row {row_idx + 1}: expected {width}, got {len(tiles)}"
        )
    return tiles


def rle_encode_row(row: List[str]) -> str:
    if not row:
        return ""
    out = []
    current = row[0]
    count = 1
    for t in row[1:]:
        if t == current:
            count += 1
        else:
            out.append(f"{current}{count}")
            current = t
            count = 1
    out.append(f"{current}{count}")
    return "".join(out)


def load_board(path: str) -> Tuple[List[List[str]], int, int]:
    with open(path, "r", encoding="utf-8") as f:
        lines = [ln.rstrip("\n") for ln in f.readlines()]
    if not lines:
        raise ValueError("Empty file")
    width, height = parse_dimensions(lines[0])
    if len(lines) - 1 != height:
        raise ValueError(
            f"Height mismatch: expected {height} rows, got {len(lines) - 1}"
        )
    board: List[List[str]] = []
    for r in range(height):
        row_tiles = rle_decode_row(lines[r + 1], width, r)
        board.append(row_tiles)
    return board, width, height


def save_board(path: str, board: List[List[str]]) -> None:
    height = len(board)
    width = len(board[0]) if height > 0 else 0

    with open(path, "w", encoding="utf-8") as f:
        f.write(f"{width}x{height}\n")
        for r in range(height):
            f.write(rle_encode_row(board[r]) + "\n")


BG = (30, 30, 36)
GRID = (60, 60, 72)
GRID_LIGHT = (80, 80, 96)
TEXT = (230, 230, 235)
PANEL_BG = (18, 18, 22)
BTN_BG = (45, 45, 55)
BTN_BG_HOVER = (62, 62, 76)
BTN_BG_ACTIVE = (90, 90, 110)

COLORS = {
    "E": (40, 40, 48),
    "W": (90, 90, 90),
    "A": (220, 90, 70),
    "B": (70, 120, 220),
}

GRID_5 = (110, 110, 130)
GRID_10 = (160, 160, 180)

DEFAULT_MIN_W = 1440
DEFAULT_MIN_H = 900
MIN_CELL_PX = 16
MAX_CELL_PX = 128

# UI paddings
PANEL_PAD = 12
BTN_PAD_X = 12
BTN_PAD_Y = 8
SWATCH_SIZE = 20
SWATCH_GAP = 8
BTN_HEIGHT = 40
BTN_SPACING = 8
HELP_PAD = 20
MSG_PAD_X = 8
MSG_PAD_Y = 6

# Scrollbars
SCROLL_THICK = 12
SCROLL_MIN_THUMB = 32
SCROLL_TRACK = (50, 50, 60)
SCROLL_THUMB = (120, 120, 140)
SCROLL_SPEED = 60  # pixels per wheel tick


def auto_cell_size(width: int, height: int, panel_w: int = 220) -> int:
    width = max(1, min(100, width))
    height = max(1, min(100, height))
    avail_w = max(1, DEFAULT_MIN_W - panel_w)
    avail_h = max(1, DEFAULT_MIN_H)
    cell_w = avail_w // width
    cell_h = avail_h // height
    cell = max(MIN_CELL_PX, min(MAX_CELL_PX, min(cell_w, cell_h)))
    return cell


def clamp(v: int, lo: int, hi: int) -> int:
    if hi < lo:
        return 0
    return max(lo, min(hi, v))


class Editor:
    def __init__(
        self,
        width: int,
        height: int,
        board: Optional[List[List[str]]] = None,
        load_path: Optional[str] = None,
        out_path: Optional[str] = None,
        cell_size: int = 0,
        show_grid: bool = True,
        palette_on_right: bool = False,
        window_title: str = "Board Editor",
    ) -> None:
        pygame.init()
        pygame.display.set_caption(window_title)

        self.width = width
        self.height = height
        self.panel_w = 250

        self.load_path = load_path
        self.out_path = out_path
        self.cell = (
            auto_cell_size(width, height, self.panel_w)
            if int(cell_size) <= 0
            else max(MIN_CELL_PX, min(MAX_CELL_PX, int(cell_size)))
        )
        self.show_grid = show_grid
        self.palette_right = palette_on_right

        if board is None:
            self.board = [["E" for _ in range(width)] for _ in range(height)]
        else:
            self.board = board

        self._dedupe_players()

        self.font = ft.Font(None, 20)
        self.font_small = ft.Font(None, 16)
        self.help_visible = True

        self.current_tool = "W"
        self.mouse_down = False
        self.last_painted = set()

        self.scroll_x = 0
        self.scroll_y = 0
        self._drag_kind: Optional[str] = None  # 'h' or 'v'
        self._drag_offset = 0  # px from thumb corner at click time

        self.win_w = max(self.width * self.cell + self.panel_w, DEFAULT_MIN_W)
        self.win_h = max(self.height * self.cell, DEFAULT_MIN_H)
        self._recompute_layout()
        self.screen = pygame.display.set_mode(
            (self.win_w, self.win_h), pygame.RESIZABLE
        )

        self.clock = pygame.time.Clock()
        self.message: Optional[str] = None
        self.message_timer = 0

        self._metrics = {}

    def _dedupe_players(self) -> None:
        seen_a = False
        seen_b = False
        for r in range(self.height):
            for c in range(self.width):
                if self.board[r][c] == "A":
                    if seen_a:
                        self.board[r][c] = "E"
                    else:
                        seen_a = True
                elif self.board[r][c] == "B":
                    if seen_b:
                        self.board[r][c] = "E"
                    else:
                        seen_b = True

    def _recompute_layout(self) -> None:
        panel_left = self.win_w - self.panel_w if self.palette_right else 0
        self.panel_rect = pygame.Rect(panel_left, 0, self.panel_w, self.win_h)

    def _compute_metrics(self):
        grid_w = self.width * self.cell
        grid_h = self.height * self.cell

        base_vx = 0 if self.palette_right else self.panel_w
        base_vy = 0
        base_vw = self.win_w - self.panel_w
        base_vh = self.win_h

        need_h = grid_w > base_vw
        need_v = grid_h > base_vh

        while True:
            eff_vw = base_vw - (SCROLL_THICK if need_v else 0)
            eff_vh = base_vh - (SCROLL_THICK if need_h else 0)
            new_need_h = grid_w > eff_vw
            new_need_v = grid_h > eff_vh
            if new_need_h == need_h and new_need_v == need_v:
                break
            need_h, need_v = new_need_h, new_need_v

        eff_vw = base_vw - (SCROLL_THICK if need_v else 0)
        eff_vh = base_vh - (SCROLL_THICK if need_h else 0)
        viewport = pygame.Rect(base_vx, base_vy, eff_vw, eff_vh)

        if not need_h and not need_v:
            gx = viewport.x + (viewport.w - grid_w) // 2
            gy = viewport.y + (viewport.h - grid_h) // 2
            max_sx = 0
            max_sy = 0
            self.scroll_x = 0
            self.scroll_y = 0
        else:
            gx = viewport.x
            gy = viewport.y
            max_sx = max(0, grid_w - viewport.w)
            max_sy = max(0, grid_h - viewport.h)
            self.scroll_x = clamp(self.scroll_x, 0, max_sx)
            self.scroll_y = clamp(self.scroll_y, 0, max_sy)

        h_track = v_track = h_thumb = v_thumb = None
        if need_h:
            h_track = pygame.Rect(
                viewport.x, viewport.y + viewport.h, viewport.w, SCROLL_THICK
            )
            ratio = viewport.w / grid_w
            thumb_w = max(SCROLL_MIN_THUMB, int(viewport.w * ratio))
            free = viewport.w - thumb_w
            thumb_x = (
                viewport.x
                if max_sx == 0
                else viewport.x + int(free * (self.scroll_x / max_sx))
            )
            h_thumb = pygame.Rect(thumb_x, h_track.y, thumb_w, SCROLL_THICK)

        if need_v:
            v_track = pygame.Rect(
                viewport.x + viewport.w, viewport.y, SCROLL_THICK, viewport.h
            )
            ratio = viewport.h / grid_h
            thumb_h = max(SCROLL_MIN_THUMB, int(viewport.h * ratio))
            free = viewport.h - thumb_h
            thumb_y = (
                viewport.y
                if max_sy == 0
                else viewport.y + int(free * (self.scroll_y / max_sy))
            )
            v_thumb = pygame.Rect(v_track.x, thumb_y, SCROLL_THICK, thumb_h)

        metrics = {
            "grid_w": grid_w,
            "grid_h": grid_h,
            "viewport": viewport,
            "grid_origin": (gx, gy),
            "need_h": need_h,
            "need_v": need_v,
            "max_scroll_x": max_sx,
            "max_scroll_y": max_sy,
            "h_track": h_track,
            "v_track": v_track,
            "h_thumb": h_thumb,
            "v_thumb": v_thumb,
        }
        self._metrics = metrics
        return metrics

    def _recompute_window_size(self) -> None:
        grid_w = self.width * self.cell
        grid_h = self.height * self.cell
        self.win_w = max(grid_w + self.panel_w, DEFAULT_MIN_W)
        self.win_h = max(grid_h, DEFAULT_MIN_H)
        panel_left = self.win_w - self.panel_w if self.palette_right else 0
        self.panel_rect = pygame.Rect(panel_left, 0, self.panel_w, self.win_h)

    def _pos_to_cell(self, mx: int, my: int) -> Optional[Tuple[int, int]]:
        m = self._metrics or self._compute_metrics()
        vx, vy, vw, vh = m["viewport"]
        gx, gy = m["grid_origin"]
        if mx < gx or my < gy or mx >= gx + vw or my >= gy + vh:
            return None
        local_x = (mx - gx) + (self.scroll_x if (m["need_h"] or m["need_v"]) else 0)
        local_y = (my - gy) + (self.scroll_y if (m["need_h"] or m["need_v"]) else 0)
        c = local_x // self.cell
        r = local_y // self.cell
        if r < 0 or r >= self.height or c < 0 or c >= self.width:
            return None
        return int(r), int(c)

    def show_msg(self, text: str, seconds: float = 2.0) -> None:
        self.message = text
        self.message_timer = int(seconds * 60)

    def _render_surface(
        self, font: ft.Font, text: str, color: Tuple[int, int, int]
    ) -> pygame.Surface:
        surf, _ = font.render(text, color)
        return surf

    def set_tile(self, r: int, c: int, t: str) -> None:
        if t == "A":
            for rr in range(self.height):
                for cc in range(self.width):
                    if self.board[rr][cc] == "A":
                        self.board[rr][cc] = "E"
        elif t == "B":
            for rr in range(self.height):
                for cc in range(self.width):
                    if self.board[rr][cc] == "B":
                        self.board[rr][cc] = "E"
        self.board[r][c] = t

    def paint_at(self, r: int, c: int, right_click: bool = False) -> None:
        key = (r, c)
        if key in self.last_painted:
            return
        self.last_painted.add(key)
        if right_click:
            self.board[r][c] = "E"
        else:
            self.set_tile(r, c, self.current_tool)

    def _draw_scrollbars(self, surface: pygame.Surface, m):
        if m["need_h"]:
            pygame.draw.rect(surface, SCROLL_TRACK, m["h_track"])
            pygame.draw.rect(surface, SCROLL_THUMB, m["h_thumb"], border_radius=4)
        if m["need_v"]:
            pygame.draw.rect(surface, SCROLL_TRACK, m["v_track"])
            pygame.draw.rect(surface, SCROLL_THUMB, m["v_thumb"], border_radius=4)
        # corner box when both scrollbars exist
        if m["need_h"] and m["need_v"]:
            corner = pygame.Rect(
                m["v_track"].x, m["h_track"].y, SCROLL_THICK, SCROLL_THICK
            )
            pygame.draw.rect(surface, SCROLL_TRACK, corner)

    def draw_grid(self, surface: pygame.Surface) -> None:
        m = self._compute_metrics()
        gx, gy = m["grid_origin"]
        viewport = m["viewport"]

        # Determine visible tile range
        if m["need_h"] or m["need_v"]:
            start_c = self.scroll_x // self.cell
            start_r = self.scroll_y // self.cell
            end_c = min(
                self.width, (self.scroll_x + viewport.w + self.cell - 1) // self.cell
            )
            end_r = min(
                self.height, (self.scroll_y + viewport.h + self.cell - 1) // self.cell
            )
        else:
            start_c, start_r = 0, 0
            end_c, end_r = self.width, self.height

        # Tiles
        for r in range(start_r, end_r):
            for c in range(start_c, end_c):
                t = self.board[r][c]
                color = COLORS.get(t, (100, 100, 100))
                px = gx + (c * self.cell - self.scroll_x)
                py = gy + (r * self.cell - self.scroll_y)
                pygame.draw.rect(surface, color, (px, py, self.cell, self.cell))

        # Grid lines
        if self.show_grid and self.cell >= 10:
            # Horizontal lines
            first_hr = start_r
            last_hr = end_r
            for r in range(first_hr, last_hr + 1):
                y = gy + (r * self.cell - self.scroll_y)
                if r % 10 == 0:
                    col, w = GRID_10, 3 if self.cell >= 24 else 2
                elif r % 5 == 0:
                    col, w = GRID_5, 2 if self.cell >= 20 else 1
                else:
                    col, w = GRID, 1
                pygame.draw.line(
                    surface,
                    col,
                    (gx + (start_c * self.cell - self.scroll_x), y),
                    (gx + (end_c * self.cell - self.scroll_x), y),
                    w,
                )

            # Vertical lines
            first_vc = start_c
            last_vc = end_c
            for c in range(first_vc, last_vc + 1):
                x = gx + (c * self.cell - self.scroll_x)
                if c % 10 == 0:
                    col, w = GRID_10, 3 if self.cell >= 24 else 2
                elif c % 5 == 0:
                    col, w = GRID_5, 2 if self.cell >= 20 else 1
                else:
                    col, w = GRID, 1
                pygame.draw.line(
                    surface,
                    col,
                    (x, gy + (start_r * self.cell - self.scroll_y)),
                    (x, gy + (end_r * self.cell - self.scroll_y)),
                    w,
                )

        # Hover highlight
        mx, my = pygame.mouse.get_pos()
        cell = self._pos_to_cell(mx, my)
        if cell:
            r, c = cell
            px = gx + (c * self.cell - self.scroll_x)
            py = gy + (r * self.cell - self.scroll_y)
            pygame.draw.rect(
                surface, GRID_LIGHT, (px, py, self.cell, self.cell), width=2
            )

        # Scrollbars
        self._draw_scrollbars(surface, m)

    def draw_panel(self, surface: pygame.Surface) -> None:
        panel_x = self.win_w - self.panel_w if self.palette_right else 0
        panel = pygame.Rect(panel_x, 0, self.panel_w, self.win_h)
        pygame.draw.rect(surface, PANEL_BG, panel)

        title_surf = self._render_surface(self.font, "Board Editor", TEXT)
        surface.blit(title_surf, (panel.left + PANEL_PAD, PANEL_PAD))

        btn_w = self.panel_w - 2 * PANEL_PAD
        start_y = PANEL_PAD + title_surf.get_height() + BTN_SPACING

        tools = [
            ("Empty (E)", "E"),
            ("Wall (W)", "W"),
            ("Player 1 (A)", "A"),
            ("Player 2 (B)", "B"),
        ]
        for i, (label, token) in enumerate(tools):
            rect = pygame.Rect(
                panel.left + PANEL_PAD,
                start_y + i * (BTN_HEIGHT + BTN_SPACING),
                btn_w,
                BTN_HEIGHT,
            )
            mouse_over = rect.collidepoint(pygame.mouse.get_pos())
            active = self.current_tool == token
            bg = BTN_BG_ACTIVE if active else (BTN_BG_HOVER if mouse_over else BTN_BG)
            pygame.draw.rect(surface, bg, rect, border_radius=8)

            sw_y = rect.top + (rect.height - SWATCH_SIZE) // 2
            sw = pygame.Rect(rect.left + BTN_PAD_X, sw_y, SWATCH_SIZE, SWATCH_SIZE)
            pygame.draw.rect(surface, COLORS[token], sw, border_radius=4)

            label_surf = self._render_surface(self.font, label, TEXT)
            lx = sw.right + SWATCH_GAP
            ly = rect.top + (rect.height - label_surf.get_height()) // 2
            max_label_w = rect.right - BTN_PAD_X - lx
            if label_surf.get_width() > max_label_w:
                ell = "…"
                base = label
                while (
                    base
                    and self._render_surface(self.font, base + ell, TEXT).get_width()
                    > max_label_w
                ):
                    base = base[:-1]
                label_surf = self._render_surface(
                    self.font, (base + ell) if base else ell, TEXT
                )
            surface.blit(label_surf, (lx, ly))

            if mouse_over and pygame.mouse.get_pressed()[0]:
                self.current_tool = token

        a_count = sum(t == "A" for row in self.board for t in row)
        b_count = sum(t == "B" for row in self.board for t in row)
        info_start_y = start_y + len(tools) * (BTN_HEIGHT + BTN_SPACING) + BTN_SPACING
        info_lines = [
            f"Size: {self.width}x{self.height}",
            f"A placed: {a_count}/1",
            f"B placed: {b_count}/1",
            f"Cell: {self.cell}px",
            f"Grid: {'on' if self.show_grid else 'off'}",
            f"Out: {self.out_path or self.load_path or '(press S to save)'}",
        ]
        y_cursor = info_start_y
        for line in info_lines:
            ls = self._render_surface(self.font_small, line, TEXT)
            surface.blit(ls, (panel.left + PANEL_PAD, y_cursor))
            y_cursor += ls.get_height() + 2

        hint_surf = self._render_surface(self.font_small, "Press H for help", TEXT)
        surface.blit(
            hint_surf,
            (panel.left + PANEL_PAD, self.win_h - PANEL_PAD - hint_surf.get_height()),
        )

        if self.message and self.message_timer > 0:
            msg_surf = self._render_surface(
                self.font_small, self.message, (255, 200, 200)
            )
            msg_w = msg_surf.get_width() + 2 * MSG_PAD_X
            msg_h = msg_surf.get_height() + 2 * MSG_PAD_Y
            msg_rect = pygame.Rect(
                panel.left + PANEL_PAD,
                self.win_h - PANEL_PAD - hint_surf.get_height() - BTN_SPACING - msg_h,
                msg_w,
                msg_h,
            )
            pygame.draw.rect(surface, (60, 30, 30), msg_rect, border_radius=6)
            surface.blit(
                msg_surf, (msg_rect.left + MSG_PAD_X, msg_rect.top + MSG_PAD_Y)
            )

    def draw_help(self, surface: pygame.Surface) -> None:
        overlay = pygame.Surface((self.win_w, self.win_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))

        lines = [
            "",
            "Controls:",
            "  [Left click] to paint, [Right click] to erase,  ",
            "",
            "Tools:",
            "  [E] Empty, [W] Wall, [1/A] Player 1, [2/B] Player 2  ",
            "",
            "Hotkeys:",
            "  [S] Save, [G] Toggle grid, [+/-] Zoom in/out,  ",
            "  [H] Show help, [Backspace] Quit  ",
            "",
            "  Note that both players must be placed  ",
            "  for the world to be playable.  ",
            "",
        ]

        line_surfs = [
            self._render_surface(self.font, ln, (255, 255, 255)) for ln in lines
        ]
        max_w = max(s.get_width() for s in line_surfs)
        total_h = sum(s.get_height() for s in line_surfs) + (len(line_surfs) - 1) * 6

        box_w = max_w + 2 * HELP_PAD
        box_h = total_h + 2 * HELP_PAD
        box_x = (self.win_w - box_w) // 2
        box_y = (self.win_h - box_h) // 2

        pygame.draw.rect(
            surface, (50, 50, 60), (box_x, box_y, box_w, box_h), border_radius=12
        )

        y = box_y + HELP_PAD
        for s in line_surfs:
            x = box_x + (box_w - s.get_width()) // 2
            surface.blit(s, (x, y))
            y += s.get_height() + 6

    def _handle_scroll_drag(self, event):
        m = self._metrics
        if not m:
            return
        if self._drag_kind == "h" and m["h_track"]:
            thumb = m["h_thumb"]
            track = m["h_track"]
            new_x = clamp(
                event.pos[0] - self._drag_offset, track.x, track.right - thumb.w
            )
            thumb.x = new_x
            free = track.w - thumb.w
            self.scroll_x = (
                0 if free == 0 else int((new_x - track.x) * m["max_scroll_x"] / free)
            )
        elif self._drag_kind == "v" and m["v_track"]:
            thumb = m["v_thumb"]
            track = m["v_track"]
            new_y = clamp(
                event.pos[1] - self._drag_offset, track.y, track.bottom - thumb.h
            )
            thumb.y = new_y
            free = track.h - thumb.h
            self.scroll_y = (
                0 if free == 0 else int((new_y - track.y) * m["max_scroll_y"] / free)
            )

    def run(self) -> None:
        running = True
        while running:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.VIDEORESIZE:
                    new_w = max(event.w, DEFAULT_MIN_W)
                    new_h = max(event.h, DEFAULT_MIN_H)
                    self.win_w, self.win_h = new_w, new_h
                    self._recompute_layout()
                    if (new_w, new_h) != (event.w, event.h):
                        self.screen = pygame.display.set_mode(
                            (self.win_w, self.win_h), pygame.RESIZABLE
                        )
                elif event.type == pygame.MOUSEWHEEL:
                    mods = pygame.key.get_mods()
                    horiz = (mods & pygame.KMOD_SHIFT) or (getattr(event, "x", 0) != 0)
                    if horiz:
                        dx = getattr(event, "x", 0)
                        if dx == 0:
                            dx = event.y  # shift+wheel
                        self.scroll_x = clamp(
                            self.scroll_x - dx * SCROLL_SPEED,
                            0,
                            self._metrics.get("max_scroll_x", 0),
                        )
                    else:
                        self.scroll_y = clamp(
                            self.scroll_y - event.y * SCROLL_SPEED,
                            0,
                            self._metrics.get("max_scroll_y", 0),
                        )
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.help_visible:
                        self.help_visible = False
                    m = self._metrics or self._compute_metrics()
                    if event.button in (1,):
                        # Scrollbar hit-testing first
                        if (
                            m["need_h"]
                            and m["h_thumb"]
                            and m["h_thumb"].collidepoint(event.pos)
                        ):
                            self._drag_kind = "h"
                            self._drag_offset = event.pos[0] - m["h_thumb"].x
                            continue
                        if (
                            m["need_v"]
                            and m["v_thumb"]
                            and m["v_thumb"].collidepoint(event.pos)
                        ):
                            self._drag_kind = "v"
                            self._drag_offset = event.pos[1] - m["v_thumb"].y
                            continue
                        # Click in tracks to jump
                        if (
                            m["need_h"]
                            and m["h_track"]
                            and m["h_track"].collidepoint(event.pos)
                            and not m["h_thumb"].collidepoint(event.pos)
                        ):
                            rel = (event.pos[0] - m["h_track"].x) / max(
                                1, m["h_track"].w
                            )
                            self.scroll_x = int(rel * m["max_scroll_x"])
                        elif (
                            m["need_v"]
                            and m["v_track"]
                            and m["v_track"].collidepoint(event.pos)
                            and not m["v_thumb"].collidepoint(event.pos)
                        ):
                            rel = (event.pos[1] - m["v_track"].y) / max(
                                1, m["v_track"].h
                            )
                            self.scroll_y = int(rel * m["max_scroll_y"])
                        else:
                            # Painting
                            self.mouse_down = True
                            self.last_painted.clear()
                            cell = self._pos_to_cell(*event.pos)
                            if cell is not None:
                                r, c = cell
                                self.paint_at(r, c, right_click=False)
                    elif event.button == 3:
                        self.mouse_down = True
                        self.last_painted.clear()
                        cell = self._pos_to_cell(*event.pos)
                        if cell is not None:
                            r, c = cell
                            self.paint_at(r, c, right_click=True)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button in (1, 3):
                        self.mouse_down = False
                        self.last_painted.clear()
                        self._drag_kind = None
                elif event.type == pygame.MOUSEMOTION:
                    if self._drag_kind:
                        self._handle_scroll_drag(event)
                    elif self.mouse_down:
                        buttons = pygame.mouse.get_pressed()
                        right = buttons[2]
                        cell = self._pos_to_cell(*event.pos)
                        if cell is not None:
                            r, c = cell
                            self.paint_at(r, c, right_click=right)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    elif event.key in (pygame.K_h, pygame.K_QUESTION):
                        self.help_visible = not self.help_visible
                    elif event.key == pygame.K_g:
                        if self.help_visible:
                            self.help_visible = False
                        self.show_grid = not self.show_grid
                    elif event.key == pygame.K_EQUALS or event.key == pygame.K_PLUS:
                        if self.help_visible:
                            self.help_visible = False
                        self.cell = min(MAX_CELL_PX, self.cell + 2)
                        self._recompute_layout()
                    elif event.key == pygame.K_MINUS:
                        if self.help_visible:
                            self.help_visible = False
                        self.cell = max(MIN_CELL_PX, self.cell - 2)
                        self._recompute_layout()
                    elif event.key in (pygame.K_e,):
                        if self.help_visible:
                            self.help_visible = False
                        self.current_tool = "E"
                    elif event.key in (pygame.K_w,):
                        if self.help_visible:
                            self.help_visible = False
                        self.current_tool = "W"
                    elif event.key in (pygame.K_1, pygame.K_a):
                        if self.help_visible:
                            self.help_visible = False
                        self.current_tool = "A"
                    elif event.key in (pygame.K_2, pygame.K_b):
                        if self.help_visible:
                            self.help_visible = False
                        self.current_tool = "B"
                    elif event.key == pygame.K_s:
                        if self.help_visible:
                            self.help_visible = False
                        try:
                            path = (
                                self.out_path
                                or self.load_path
                                or f"board_{self.width}x{self.height}.world"
                            )
                            save_board(path, self.board)
                            self.show_msg(f"Saved: {path}", seconds=2.5)
                        except Exception as ex:
                            self.show_msg(f"Save failed: {ex}", seconds=4)

            self.screen.fill(BG)
            self.draw_grid(self.screen)
            self.draw_panel(self.screen)
            if self.help_visible:
                self.draw_help(self.screen)

            if self.message_timer > 0:
                self.message_timer -= 1
                if self.message_timer == 0:
                    self.message = None

            pygame.display.flip()

        pygame.quit()


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Pygame board editor."
    )
    group = p.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--load",
        type=str,
        help="path to an existing board file to load"
    )
    group.add_argument(
        "--size",
        type=str,
        help="dimensions of new empty board, formatted as [WIDTH]x[HEIGHT] (e.g., 20x15)."
    )
    p.add_argument(
        "--out",
        type=str,
        default=None,
        help="save path used when pressing 'S'. if omitted, will save to --load path or a default name"
    )
    p.add_argument(
        "--cell",
        type=int,
        default=0,
        help="cell size in pixels (16..128). if omitted, set automatically based on board size"
    )
    p.add_argument(
        "--no-grid", action="store_true", help="hide grid lines when editor opens"
    )
    p.add_argument(
        "--palette-right",
        action="store_true",
        help="place the tool palette on the right instead of the left"
    )
    p.add_argument(
        "--title",
        type=str,
        default="Board Editor",
        help="window title"
    )
    return p


def main():
    args = build_arg_parser().parse_args()

    if args.load:
        board, w, h = load_board(args.load)
        editor = Editor(
            w,
            h,
            board=board,
            load_path=args.load,
            out_path=args.out,
            cell_size=args.cell,
            show_grid=not args.no_grid,
            palette_on_right=args.palette_right,
            window_title=args.title,
        )
    else:
        w, h = parse_dimensions(args.size)
        board = [["E" for _ in range(w)] for _ in range(h)]
        editor = Editor(
            w,
            h,
            board=board,
            out_path=args.out,
            cell_size=args.cell,
            show_grid=not args.no_grid,
            palette_on_right=args.palette_right,
            window_title=args.title,
        )

    editor.run()


if __name__ == "__main__":
    main()
