"""Statistics calculation service."""

from typing import Dict
from models import Collection, PartType


class StatsService:
    """Service for calculating collection statistics."""
    
    @staticmethod
    def generate_stats_text(collection: Collection) -> str:
        """Calculate and format collection statistics."""
        total_parts = len(collection.parts)
        total_quantity = sum(part.owned_quantity for part in collection.parts)
        
        blades = collection.get_parts_by_type(PartType.BLADE)
        ratchets = collection.get_parts_by_type(PartType.RATCHET)
        bits = collection.get_parts_by_type(PartType.BIT)
        
        # Rarity breakdown
        rarity_counts = {}
        for part in collection.parts:
            rarity = part.rarity.value
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + part.owned_quantity
        
        stats_content = f"""🌪️ BEYBLADE X COLLECTION STATISTICS 🌪️

📦 COLLECTION OVERVIEW:
• Total Unique Parts: {total_parts}
• Total Parts Owned: {total_quantity}
• Total Combos Created: {len(collection.combos)}

🔧 PARTS BREAKDOWN:
• Blades: {len(blades)} unique ({sum(b.owned_quantity for b in blades)} total)
• Ratchets: {len(ratchets)} unique ({sum(r.owned_quantity for r in ratchets)} total)
• Bits: {len(bits)} unique ({sum(b.owned_quantity for b in bits)} total)

✨ RARITY BREAKDOWN:
"""
        
        for rarity, count in rarity_counts.items():
            stats_content += f"• {rarity}: {count} parts\n"
        
        if collection.parts:
            # Weight statistics
            parts_with_weight = [p for p in collection.parts if p.weight]
            if parts_with_weight:
                total_weight = sum(p.weight * p.owned_quantity for p in parts_with_weight)
                avg_weight = sum(p.weight for p in parts_with_weight) / len(parts_with_weight)
                
                stats_content += f"""
⚖️ WEIGHT STATISTICS:
• Total Collection Weight: {total_weight:.1f}g
• Average Part Weight: {avg_weight:.1f}g
"""
        
        # Most owned parts
        if collection.parts:
            most_owned = max(collection.parts, key=lambda p: p.owned_quantity)
            stats_content += f"""
🏆 COLLECTION HIGHLIGHTS:
• Most Owned Part: {most_owned.name} ({most_owned.owned_quantity} copies)
"""
        
        return stats_content
