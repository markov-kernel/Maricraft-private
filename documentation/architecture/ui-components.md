# UI Component Architecture

> Maricraft uses CustomTkinter for its modern GUI. The UI is organized into reusable components.

## Overview

The UI is built with CustomTkinter, a modern themed wrapper around Tkinter. All components follow a consistent pattern and share styling through a central theme module.

## Component Structure

```
maricraft/ui/
├── __init__.py              # Package exports
├── app.py                   # Main App class (entry point)
├── state.py                 # JSON state persistence
├── theme.py                 # Color/font definitions
└── components/
    ├── __init__.py          # Component exports
    ├── category_frame.py    # Button category containers
    ├── command_button.py    # Individual command buttons
    ├── favorites_bar.py     # Quick access favorites
    ├── install_dialog.py    # Datapack installation UI
    ├── quick_toolbar.py     # Top toolbar
    ├── search_bar.py        # Command search
    ├── settings_dialog.py   # Settings panel
    ├── status_bar.py        # Bottom status bar
    └── tooltip.py           # Hover tooltips
```

## Key Patterns

### State Management

All settings are persisted via `state.py` to a JSON file:

```python
from maricraft.ui.state import AppState

state = AppState()
state.favorites = ["Full Heal", "Diamond Armor"]
state.save()  # Persists to ~/.maricraft/state.json
```

**Persisted Settings:**
- Window position and size
- Favorite commands
- Last selected category
- User preferences (delay, chat key)

### Theming

Colors and fonts are defined in `theme.py` and referenced by all components:

```python
from maricraft.ui.theme import COLORS, FONTS

button = ctk.CTkButton(
    fg_color=COLORS["primary"],
    font=FONTS["button"]
)
```

**Color Palette:**
| Key | Purpose |
|-----|---------|
| `primary` | Main accent color |
| `secondary` | Secondary buttons |
| `background` | Window background |
| `surface` | Card/panel backgrounds |
| `text` | Primary text |
| `text_secondary` | Muted text |

### Event Flow

```
User Click → CommandButton
                ↓
           commands.py (get command list)
                ↓
           automator.py (WindowsAutomator)
                ↓
           Minecraft (via pyautogui clipboard paste)
```

## Component Reference

### App (`app.py`)

Main application window. Handles:
- Window initialization
- Category/button layout
- Edition detection (Java vs Bedrock)
- Datapack installation coordination

### CategoryFrame (`category_frame.py`)

Container for related command buttons:

```python
CategoryFrame(
    parent=self,
    title="Buffs & Effects",
    buttons=[...],
    color="#FF6B6B"
)
```

### CommandButton (`command_button.py`)

Individual command button with:
- Hover tooltip
- Click handler
- Favorite star toggle
- Visual feedback on click

### FavoritesBar (`favorites_bar.py`)

Quick access bar showing starred commands. Updates dynamically when favorites change.

### InstallDialog (`install_dialog.py`)

Modal dialog for datapack/behavior pack installation:
- Lists available Minecraft worlds
- Shows installation status
- Handles Java/Bedrock path differences

### SearchBar (`search_bar.py`)

Command search with:
- Real-time filtering
- Fuzzy matching
- Keyboard navigation (Enter to execute)

### SettingsDialog (`settings_dialog.py`)

Configuration panel for:
- Chat key binding (default: T)
- Command delay (milliseconds)
- Update checking
- Reset to defaults

### StatusBar (`status_bar.py`)

Bottom status bar showing:
- Current edition (Java/Bedrock)
- Datapack status
- Last command sent

### Tooltip (`tooltip.py`)

Hover tooltips for buttons showing command description.

## Extending the UI

### Adding a New Component

1. Create new file in `components/`:
   ```python
   # components/my_widget.py
   import customtkinter as ctk
   from ..theme import COLORS

   class MyWidget(ctk.CTkFrame):
       def __init__(self, parent, **kwargs):
           super().__init__(parent, **kwargs)
           # Build widget...
   ```

2. Export in `components/__init__.py`:
   ```python
   from .my_widget import MyWidget
   ```

3. Integrate in `app.py`:
   ```python
   from .components import MyWidget

   class App:
       def __init__(self):
           self.my_widget = MyWidget(self.main_frame)
   ```

### Adding a New Button Category

Edit `commands.py`:

```python
CATEGORIES = {
    "New Category": {
        "color": "#9B59B6",
        "buttons": [
            CommandButton(
                name="My Button",
                description="Does something cool",
                commands=["/say Hello"],
                function_id="maricraft:new_category/my_button"
            )
        ]
    }
}
```

## Related Documentation

- [CLAUDE.md](../../CLAUDE.md) - Developer quick reference
- [TECHNICAL.md](../../TECHNICAL.md) - Deep technical documentation
