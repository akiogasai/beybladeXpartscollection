"""Business logic for part operations."""

from typing import List, Optional
from models import BeybladePart, PartType, Collection
from data import get_all_parts, find_database_part, BEYBLADE_X_DATABASE, save_collection, load_collection


class PartService:
    """Service for part-related operations."""
    
    def __init__(self):
        """Initialize the part service with a collection."""
        self._collection = Collection()
    
    def get_collection(self) -> Collection:
        """Get the current collection."""
        return self._collection
    
    def get_database(self) -> dict:
        """Get the parts database."""
        return BEYBLADE_X_DATABASE
    
    def load_collection(self, filename: str):
        """Load collection from file."""
        self._collection = load_collection(filename)
    
    def save_collection(self, filename: str):
        """Save collection to file."""
        save_collection(self._collection, filename)
    
    @staticmethod
    def filter_parts(parts: List[BeybladePart], search_term: str = "", part_type_filter: str = "All") -> List[BeybladePart]:
        """Filter parts by search term and type."""
        filtered = parts
        
        if part_type_filter != "All":
            filtered = [p for p in filtered if p.part_type.value == part_type_filter]
        
        if search_term:
            search_lower = search_term.lower()
            filtered = [p for p in filtered if search_lower in p.name.lower()]
        
        return filtered
    
    @staticmethod
    def create_part_from_database(name: str, part_type: PartType, quantity: int, condition: str) -> Optional[BeybladePart]:
        """Create a new part instance from database template."""
        db_part = find_database_part(name, part_type)
        if db_part:
            return BeybladePart(
                name=db_part.name,
                part_type=db_part.part_type,
                series=db_part.series,
                rarity=db_part.rarity,
                weight=db_part.weight,
                description=db_part.description,
                owned_quantity=quantity,
                condition=condition
            )
        return None
