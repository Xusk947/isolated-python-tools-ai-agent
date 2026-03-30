TEXT_FONT_FAMILY = "Lato"
HEADING_FONT_FAMILY = "Unbounded"

TEXT_FONT_STACK = [
    TEXT_FONT_FAMILY,
    "Inter",
    "DejaVu Sans",
    "Arial",
    "Helvetica",
    "sans-serif",
]

HEADING_FONT_STACK = [
    HEADING_FONT_FAMILY,
    TEXT_FONT_FAMILY,
    "Inter",
    "DejaVu Sans",
    "Arial",
    "Helvetica",
    "sans-serif",
]

COLOR_TEXT_HEX = "#111827"
COLOR_MUTED_HEX = "#6B7280"
COLOR_BORDER_HEX = "#E5E7EB"
COLOR_BACKGROUND_HEX = "#FFFFFF"
COLOR_GRID_HEX = "#EEF0F3"

CHART_COLORWAY_HEX = [
    "#007AFF",
    "#34C759",
    "#FF9500",
    "#AF52DE",
    "#FF2D55",
    "#5AC8FA",
]


def _parse_hex(hex_color: str) -> tuple[int, int, int]:
    c = hex_color.strip().lstrip("#")
    if len(c) != 6:
        raise ValueError("invalid color")
    return (int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16))


def hex_to_rgb_float(hex_color: str) -> tuple[float, float, float]:
    r, g, b = _parse_hex(hex_color)
    return (r / 255.0, g / 255.0, b / 255.0)


def hex_to_rgb_int(hex_color: str) -> tuple[int, int, int]:
    return _parse_hex(hex_color)
