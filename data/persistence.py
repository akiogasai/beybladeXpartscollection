"""Collection persistence to JSON files."""

import json
from typing import Tuple
from models import Collection, BeybladePart, BeybladeCombo


def save_collection(collection: Collection, filename: str = "collection.json") -> None:
    """Save collection to JSON file."""
    data = {
        'parts': [part.to_dict() for part in collection.parts],
        'combos': [combo.to_dict() for combo in collection.combos]
    }
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)


def load_collection(filename: str = "collection.json") -> Collection:
    """Load collection from JSON file."""
    collection = Collection()
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        collection.parts = [BeybladePart.from_dict(part_data) for part_data in data.get('parts', [])]
        collection.combos = [BeybladeCombo.from_dict(combo_data) for combo_data in data.get('combos', [])]
    except (FileNotFoundError, json.JSONDecodeError):
        pass  # Return empty collection if file doesn't exist or is invalid
    return collection
