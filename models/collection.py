"""Collection management for Beyblade parts and combos."""

from typing import List, Optional
from .part import BeybladePart
from .combo import BeybladeCombo
from .enums import PartType


class Collection:
    def __init__(self):
        self.parts: List[BeybladePart] = []
        self.combos: List[BeybladeCombo] = []
    
    def add_part(self, part: BeybladePart) -> None:
        existing = self.find_part(part.name, part.part_type)
        if existing:
            existing.owned_quantity += part.owned_quantity
        else:
            self.parts.append(part)
    
    def remove_part(self, name: str, part_type: PartType, quantity: int = 1) -> bool:
        part = self.find_part(name, part_type)
        if part and part.owned_quantity >= quantity:
            part.owned_quantity -= quantity
            if part.owned_quantity == 0:
                self.parts.remove(part)
            return True
        return False
    
    def find_part(self, name: str, part_type: PartType) -> Optional[BeybladePart]:
        for part in self.parts:
            if part.name == name and part.part_type == part_type:
                return part
        return None
    
    def get_parts_by_type(self, part_type: PartType) -> List[BeybladePart]:
        return [part for part in self.parts if part.part_type == part_type]
    
    def add_combo(self, combo: BeybladeCombo) -> None:
        self.combos.append(combo)
    
    def remove_combo(self, combo_name: str) -> bool:
        for i, combo in enumerate(self.combos):
            if combo.name == combo_name:
                del self.combos[i]
                return True
        return False
