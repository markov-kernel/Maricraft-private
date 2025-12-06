"""Theme configuration for Maricraft - Kid-friendly colorful design."""

from __future__ import annotations

# Kid-friendly color palette
COLORS = {
    # Primary colors
    "primary": "#4A90D9",       # Friendly blue
    "secondary": "#9B59B6",     # Playful purple
    "success": "#27AE60",       # Grass green
    "warning": "#F39C12",       # Sunny orange
    "danger": "#E74C3C",        # Alert red

    # Background colors
    "background": "#1A1A2E",    # Deep dark blue
    "surface": "#16213E",       # Slightly lighter
    "surface_light": "#1F3460", # Card/panel bg

    # Text colors
    "text": "#FFFFFF",          # Main text
    "text_secondary": "#A0A0A0", # Muted text
    "text_dark": "#000000",     # Dark text on light bg

    # Accent colors
    "favorite": "#FFD700",      # Gold star
    "hover": "#5DADE2",         # Hover highlight

    # Category-specific colors (kept from original for familiarity)
    "category_buffs": "#4ECDC4",     # Teal
    "category_gear": "#9B59B6",      # Purple
    "category_teleport": "#3498DB",  # Blue
    "category_world": "#F39C12",     # Orange
}

# Map category names to their colors
CATEGORY_COLORS = {
    "Buffs & Effects": COLORS["category_buffs"],
    "Gear & Items": COLORS["category_gear"],
    "Teleport & Locate": COLORS["category_teleport"],
    "World Control": COLORS["category_world"],
}

# Font configurations (Segoe UI is clean and kid-friendly on Windows)
FONTS = {
    "title": ("Segoe UI", 24, "bold"),
    "heading": ("Segoe UI", 16, "bold"),
    "button": ("Segoe UI", 12, "bold"),
    "button_small": ("Segoe UI", 10, "bold"),
    "body": ("Segoe UI", 12),
    "small": ("Segoe UI", 10),
    "tiny": ("Segoe UI", 9),
}

# Spacing constants
SPACING = {
    "xs": 4,
    "sm": 8,
    "md": 12,
    "lg": 16,
    "xl": 24,
    "xxl": 32,
}

# Border radius for rounded corners
RADIUS = {
    "sm": 6,
    "md": 10,
    "lg": 15,
    "xl": 20,
}

# Window dimensions
WINDOW = {
    "default_width": 950,
    "default_height": 750,
    "min_width": 700,
    "min_height": 500,
}

# Button dimensions
BUTTON = {
    "width": 140,
    "height": 45,
    "min_columns": 2,
    "max_columns": 6,
}


def get_category_color(category_name: str) -> str:
    """Get the theme color for a category, with fallback."""
    return CATEGORY_COLORS.get(category_name, COLORS["primary"])


def calculate_text_color(bg_hex: str) -> str:
    """Calculate readable text color (black or white) based on background."""
    # Remove # if present
    bg_hex = bg_hex.lstrip("#")

    # Convert to RGB
    r = int(bg_hex[0:2], 16)
    g = int(bg_hex[2:4], 16)
    b = int(bg_hex[4:6], 16)

    # Calculate perceived brightness (ITU-R BT.709)
    brightness = (r * 299 + g * 587 + b * 114) / 1000

    return COLORS["text_dark"] if brightness > 128 else COLORS["text"]


def lighten_color(hex_color: str, amount: int = 30) -> str:
    """Lighten a hex color for hover effects."""
    hex_color = hex_color.lstrip("#")
    r = min(255, int(hex_color[0:2], 16) + amount)
    g = min(255, int(hex_color[2:4], 16) + amount)
    b = min(255, int(hex_color[4:6], 16) + amount)
    return f"#{r:02x}{g:02x}{b:02x}"


def darken_color(hex_color: str, amount: int = 30) -> str:
    """Darken a hex color for pressed effects."""
    hex_color = hex_color.lstrip("#")
    r = max(0, int(hex_color[0:2], 16) - amount)
    g = max(0, int(hex_color[2:4], 16) - amount)
    b = max(0, int(hex_color[4:6], 16) - amount)
    return f"#{r:02x}{g:02x}{b:02x}"
