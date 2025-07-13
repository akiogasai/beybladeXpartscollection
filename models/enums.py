"""Enums for Beyblade X types and rarities."""

from enum import Enum


class PartType(Enum):
    BLADE = "Blade"
    RATCHET = "Ratchet"
    BIT = "Bit"


class Rarity(Enum):
    COMMON = "Common"
    RARE = "Rare"
    SUPER_RARE = "Super Rare"
    ULTRA_RARE = "Ultra Rare"
