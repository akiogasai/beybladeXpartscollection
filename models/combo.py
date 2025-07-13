"""Beyblade combo model."""

from dataclasses import dataclass
from typing import Optional
from .part import BeybladePart


@dataclass
class BeybladeCombo:
    name: str
    blade: BeybladePart
    ratchet: BeybladePart
    bit: BeybladePart
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'blade': self.blade.to_dict(),
            'ratchet': self.ratchet.to_dict(),
            'bit': self.bit.to_dict(),
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'BeybladeCombo':
        return cls(
            name=data['name'],
            blade=BeybladePart.from_dict(data['blade']),
            ratchet=BeybladePart.from_dict(data['ratchet']),
            bit=BeybladePart.from_dict(data['bit']),
            notes=data.get('notes')
        )
