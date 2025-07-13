"""Beyblade part model."""

from dataclasses import dataclass
from typing import Optional
from .enums import PartType, Rarity


@dataclass
class BeybladePart:
    name: str
    part_type: PartType
    series: str
    rarity: Rarity
    weight: Optional[float] = None
    description: Optional[str] = None
    owned_quantity: int = 0
    condition: str = "New"
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'part_type': self.part_type.value,
            'series': self.series,
            'rarity': self.rarity.value,
            'weight': self.weight,
            'description': self.description,
            'owned_quantity': self.owned_quantity,
            'condition': self.condition
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BeybladePart':
        return cls(
            name=data['name'],
            part_type=PartType(data['part_type']),
            series=data['series'],
            rarity=Rarity(data['rarity']),
            weight=data.get('weight'),
            description=data.get('description'),
            owned_quantity=data.get('owned_quantity', 0),
            condition=data.get('condition', 'New')
        )
