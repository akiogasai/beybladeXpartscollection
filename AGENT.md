# Beyblade X Collection Manager

## Build/Test Commands
- **Build executable**: `build.bat` (creates PyInstaller executable in `release/`)
- **Run application**: `python main.py`
- **Run tests**: `python test_simple.py` (though test file is currently empty)
- **Test single module**: Import from models/, services/, ui/, or data/ packages

## Architecture & Structure
- **Entry point**: `main.py` - Application startup and error handling
- **Models**: `models/` - Data classes (BeybladePart, BeybladeCombo, Collection, enums)
- **Services**: `services/` - Business logic (PartService, StatsService)
- **Data**: `data/` - Database and persistence (database.py, persistence.py)
- **UI**: `ui/` - Modern Beyblade X themed interface (modern_main_window.py, modern_tabs/, theme.py)
- **Storage**: JSON file (`collection.json`) for user collection data

## Code Style & Conventions
- **Language**: Python 3.8+ with type hints and modular packages
- **Data structures**: Dataclasses with `to_dict()`/`from_dict()` serialization methods
- **Enums**: Use for controlled values (`PartType`, `Rarity`) in models/enums.py
- **Error handling**: Try/except for file operations, graceful fallbacks
- **UI patterns**: Modern card-based design with BeybladeXTheme for consistent styling
- **Services**: Business logic separated from UI in services/ package
- **Imports**: Use absolute imports (from models import..., from services import...)
- **Naming**: PascalCase for classes, snake_case for variables/methods
- **Theming**: Beyblade X official colors (blue primary, orange accent) with modern flat design
