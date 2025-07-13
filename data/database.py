"""Beyblade X parts database."""

from typing import List
from models import BeybladePart, PartType, Rarity


BEYBLADE_X_DATABASE = {
    "blades": [
        # Basic Series (BX-01 to BX-10)
        BeybladePart("Dran Sword", PartType.BLADE, "BX-01", Rarity.COMMON, 36.2, "Attack type blade with sword-like design"),
        BeybladePart("Hell's Scythe", PartType.BLADE, "BX-02", Rarity.COMMON, 32.8, "Attack type blade with scythe motif"),
        BeybladePart("Wizard Arrow", PartType.BLADE, "BX-03", Rarity.COMMON, 35.1, "Balance type blade with arrow design"),
        BeybladePart("Knight Shield", PartType.BLADE, "BX-04", Rarity.COMMON, 38.9, "Defense type blade with shield design"),
        BeybladePart("Shark Edge", PartType.BLADE, "BX-05", Rarity.COMMON, 34.7, "Attack type blade with shark fin design"),
        BeybladePart("Dran Buster", PartType.BLADE, "BX-06", Rarity.RARE, 37.3, "Enhanced version of Dran Sword"),
        BeybladePart("Phoenix Wing", PartType.BLADE, "BX-07", Rarity.RARE, 33.5, "Stamina type blade with wing design"),
        BeybladePart("Cobalt Dragoon", PartType.BLADE, "BX-08", Rarity.RARE, 36.8, "Attack type blade with dragon motif"),
        BeybladePart("Tyranno Beat", PartType.BLADE, "BX-09", Rarity.SUPER_RARE, 39.2, "Heavy attack blade with dinosaur design"),
        BeybladePart("Leon Crest", PartType.BLADE, "BX-10", Rarity.SUPER_RARE, 35.9, "Balance type blade with lion design"),
        
        # Extended Series (BX-11 to BX-20)
        BeybladePart("Viper Tail", PartType.BLADE, "BX-11", Rarity.COMMON, 34.1, "Attack type blade with viper design"),
        BeybladePart("Phoenix Feather", PartType.BLADE, "BX-12", Rarity.COMMON, 33.8, "Stamina type blade with feather motif"),
        BeybladePart("Whale Wave", PartType.BLADE, "BX-13", Rarity.RARE, 37.9, "Defense type blade with wave pattern"),
        BeybladePart("Spider Web", PartType.BLADE, "BX-14", Rarity.RARE, 35.4, "Balance type blade with web design"),
        BeybladePart("Tiger Claw", PartType.BLADE, "BX-15", Rarity.SUPER_RARE, 38.1, "Attack type blade with claw pattern"),
        BeybladePart("Eagle Eye", PartType.BLADE, "BX-16", Rarity.SUPER_RARE, 34.6, "Stamina type blade with eye design"),
        BeybladePart("Rhino Horn", PartType.BLADE, "BX-17", Rarity.RARE, 39.5, "Defense type blade with horn design"),
        BeybladePart("Wolf Fang", PartType.BLADE, "BX-18", Rarity.COMMON, 35.7, "Attack type blade with fang pattern"),
        BeybladePart("Falcon Wing", PartType.BLADE, "BX-19", Rarity.RARE, 33.2, "Balance type blade with wing design"),
        BeybladePart("Scorpion Spear", PartType.BLADE, "BX-20", Rarity.ULTRA_RARE, 40.3, "Ultimate attack blade with spear design"),
        
        # Special & Limited Editions
        BeybladePart("Dran Sword (Gold)", PartType.BLADE, "BX-01G", Rarity.ULTRA_RARE, 36.8, "Golden version of Dran Sword"),
        BeybladePart("Phoenix Wing (Crystal)", PartType.BLADE, "BX-07C", Rarity.ULTRA_RARE, 34.1, "Crystal clear Phoenix Wing"),
        BeybladePart("Leon Crest (Black)", PartType.BLADE, "BX-10B", Rarity.ULTRA_RARE, 36.4, "Black limited edition Leon Crest"),
    ],
    "ratchets": [
        # Standard Height Ratchets (60mm)
        BeybladePart("3-60", PartType.RATCHET, "Standard", Rarity.COMMON, 6.2, "3-sided ratchet, 6.0mm height"),
        BeybladePart("4-60", PartType.RATCHET, "Standard", Rarity.COMMON, 6.4, "4-sided ratchet, 6.0mm height"),
        BeybladePart("5-60", PartType.RATCHET, "Standard", Rarity.COMMON, 6.6, "5-sided ratchet, 6.0mm height"),
        BeybladePart("6-60", PartType.RATCHET, "Standard", Rarity.COMMON, 6.8, "6-sided ratchet, 6.0mm height"),
        BeybladePart("7-60", PartType.RATCHET, "Standard", Rarity.RARE, 7.0, "7-sided ratchet, 6.0mm height"),
        BeybladePart("8-60", PartType.RATCHET, "Standard", Rarity.RARE, 7.2, "8-sided ratchet, 6.0mm height"),
        BeybladePart("9-60", PartType.RATCHET, "Special", Rarity.SUPER_RARE, 8.2, "9-sided ratchet, 6.0mm height"),
        
        # Medium Height Ratchets (70mm)
        BeybladePart("3-70", PartType.RATCHET, "Standard", Rarity.COMMON, 6.8, "3-sided ratchet, 7.0mm height"),
        BeybladePart("4-70", PartType.RATCHET, "Standard", Rarity.COMMON, 7.0, "4-sided ratchet, 7.0mm height"),
        BeybladePart("5-70", PartType.RATCHET, "Standard", Rarity.COMMON, 7.2, "5-sided ratchet, 7.0mm height"),
        BeybladePart("6-70", PartType.RATCHET, "Standard", Rarity.RARE, 7.4, "6-sided ratchet, 7.0mm height"),
        BeybladePart("7-70", PartType.RATCHET, "Standard", Rarity.RARE, 7.6, "7-sided ratchet, 7.0mm height"),
        BeybladePart("8-70", PartType.RATCHET, "Standard", Rarity.SUPER_RARE, 7.8, "8-sided ratchet, 7.0mm height"),
        
        # High Height Ratchets (80mm)
        BeybladePart("3-80", PartType.RATCHET, "Standard", Rarity.RARE, 7.4, "3-sided ratchet, 8.0mm height"),
        BeybladePart("4-80", PartType.RATCHET, "Standard", Rarity.RARE, 7.6, "4-sided ratchet, 8.0mm height"),
        BeybladePart("5-80", PartType.RATCHET, "Standard", Rarity.RARE, 7.8, "5-sided ratchet, 8.0mm height"),
        BeybladePart("6-80", PartType.RATCHET, "Standard", Rarity.SUPER_RARE, 8.0, "6-sided ratchet, 8.0mm height"),
        
        # Special Ratchets
        BeybladePart("1-60", PartType.RATCHET, "Special", Rarity.ULTRA_RARE, 5.8, "Single-sided ratchet, ultra-low profile"),
        BeybladePart("2-60", PartType.RATCHET, "Special", Rarity.SUPER_RARE, 6.0, "2-sided ratchet, balanced design"),
        BeybladePart("10-75", PartType.RATCHET, "Special", Rarity.ULTRA_RARE, 8.5, "10-sided ratchet, ultimate performance"),
    ],
    "bits": [
        # Attack Type Bits
        BeybladePart("Flat", PartType.BIT, "Standard", Rarity.COMMON, 2.1, "Aggressive attack bit with flat tip"),
        BeybladePart("Rush", PartType.BIT, "Standard", Rarity.RARE, 2.6, "High-speed attack bit"),
        BeybladePart("Low Flat", PartType.BIT, "Special", Rarity.SUPER_RARE, 2.0, "Low-profile flat bit for aggressive attack"),
        BeybladePart("Xtreme", PartType.BIT, "Special", Rarity.SUPER_RARE, 2.3, "Ultra-aggressive attack bit"),
        BeybladePart("Accel", PartType.BIT, "Standard", Rarity.RARE, 2.4, "Fast attack bit with acceleration"),
        BeybladePart("Hunter", PartType.BIT, "Special", Rarity.RARE, 2.2, "Attack bit with hunting movement"),
        
        # Stamina Type Bits
        BeybladePart("Point", PartType.BIT, "Standard", Rarity.COMMON, 2.3, "Stamina bit with sharp point"),
        BeybladePart("Needle", PartType.BIT, "Standard", Rarity.RARE, 2.2, "High stamina bit with needle tip"),
        BeybladePart("Survive", PartType.BIT, "Standard", Rarity.COMMON, 2.1, "Basic stamina bit for endurance"),
        BeybladePart("Eternal", PartType.BIT, "Special", Rarity.SUPER_RARE, 2.5, "Ultimate stamina bit with free-spinning tip"),
        BeybladePart("Revolve", PartType.BIT, "Standard", Rarity.RARE, 2.3, "Stamina bit with revolving mechanism"),
        
        # Defense Type Bits
        BeybladePart("Ball", PartType.BIT, "Standard", Rarity.COMMON, 2.5, "Defense bit with ball tip"),
        BeybladePart("Defense", PartType.BIT, "Standard", Rarity.COMMON, 2.7, "Basic defense bit for stability"),
        BeybladePart("Guard", PartType.BIT, "Standard", Rarity.RARE, 2.8, "Heavy defense bit with guard ring"),
        BeybladePart("Massive", PartType.BIT, "Special", Rarity.SUPER_RARE, 3.2, "Ultra-heavy defense bit"),
        
        # Balance Type Bits
        BeybladePart("Orb", PartType.BIT, "Standard", Rarity.COMMON, 2.4, "Balance bit with orb tip"),
        BeybladePart("Taper", PartType.BIT, "Standard", Rarity.RARE, 2.4, "Balance bit with tapered tip"),
        BeybladePart("High Taper", PartType.BIT, "Special", Rarity.SUPER_RARE, 2.7, "Elevated taper bit for unique movement"),
        BeybladePart("Unite", PartType.BIT, "Special", Rarity.SUPER_RARE, 2.6, "Dual-mode balance bit"),
        BeybladePart("Variable", PartType.BIT, "Special", Rarity.RARE, 2.5, "Adaptive balance bit"),
        
        # Special & Motorized Bits
        BeybladePart("Gear Ball", PartType.BIT, "Special", Rarity.ULTRA_RARE, 3.1, "Motorized ball bit with gear mechanism"),
        BeybladePart("Motor", PartType.BIT, "Special", Rarity.ULTRA_RARE, 3.5, "Fully motorized bit for sustained spin"),
        BeybladePart("Bearing", PartType.BIT, "Special", Rarity.ULTRA_RARE, 2.8, "Precision bearing bit for maximum stamina"),
        BeybladePart("Atomic", PartType.BIT, "Special", Rarity.ULTRA_RARE, 2.9, "Free-spinning ball bit with ultimate defense"),
    ]
}


def get_all_parts() -> List[BeybladePart]:
    """Get all parts from database as a single list."""
    all_parts = []
    all_parts.extend(BEYBLADE_X_DATABASE["blades"])
    all_parts.extend(BEYBLADE_X_DATABASE["ratchets"])
    all_parts.extend(BEYBLADE_X_DATABASE["bits"])
    return all_parts


def find_database_part(name: str, part_type: PartType) -> BeybladePart:
    """Find a specific part in the database."""
    for part in get_all_parts():
        if part.name == name and part.part_type == part_type:
            return part
    return None
