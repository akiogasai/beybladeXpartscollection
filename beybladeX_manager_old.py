import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum
import os
import sys
import traceback
import logging

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('beyblade_debug.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

def handle_exception(exc_type, exc_value, exc_traceback):
    """Handle uncaught exceptions"""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    
    logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
    messagebox.showerror("Error", f"An error occurred: {exc_value}")

sys.excepthook = handle_exception

# Data Models
class PartType(Enum):
    BLADE = "Blade"
    RATCHET = "Ratchet"
    BIT = "Bit"

class Rarity(Enum):
    COMMON = "Common"
    RARE = "Rare"
    SUPER_RARE = "Super Rare"
    ULTRA_RARE = "Ultra Rare"

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
    
    def to_dict(self):
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
    def from_dict(cls, data):
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

@dataclass
class BeybladeCombo:
    name: str
    blade: BeybladePart
    ratchet: BeybladePart
    bit: BeybladePart
    notes: Optional[str] = None
    
    def to_dict(self):
        return {
            'name': self.name,
            'blade': self.blade.to_dict(),
            'ratchet': self.ratchet.to_dict(),
            'bit': self.bit.to_dict(),
            'notes': self.notes
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data['name'],
            blade=BeybladePart.from_dict(data['blade']),
            ratchet=BeybladePart.from_dict(data['ratchet']),
            bit=BeybladePart.from_dict(data['bit']),
            notes=data.get('notes')
        )

# Database
BEYBLADE_X_DATABASE = {
    "blades": [
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
    ],
    "ratchets": [
        BeybladePart("3-60", PartType.RATCHET, "Standard", Rarity.COMMON, 6.2, "3-sided ratchet, 6.0mm height"),
        BeybladePart("4-60", PartType.RATCHET, "Standard", Rarity.COMMON, 6.4, "4-sided ratchet, 6.0mm height"),
        BeybladePart("5-60", PartType.RATCHET, "Standard", Rarity.COMMON, 6.6, "5-sided ratchet, 6.0mm height"),
        BeybladePart("3-70", PartType.RATCHET, "Standard", Rarity.COMMON, 6.8, "3-sided ratchet, 7.0mm height"),
        BeybladePart("4-70", PartType.RATCHET, "Standard", Rarity.COMMON, 7.0, "4-sided ratchet, 7.0mm height"),
        BeybladePart("5-70", PartType.RATCHET, "Standard", Rarity.COMMON, 7.2, "5-sided ratchet, 7.0mm height"),
        BeybladePart("3-80", PartType.RATCHET, "Standard", Rarity.RARE, 7.4, "3-sided ratchet, 8.0mm height"),
        BeybladePart("4-80", PartType.RATCHET, "Standard", Rarity.RARE, 7.6, "4-sided ratchet, 8.0mm height"),
        BeybladePart("5-80", PartType.RATCHET, "Standard", Rarity.RARE, 7.8, "5-sided ratchet, 8.0mm height"),
        BeybladePart("9-60", PartType.RATCHET, "Special", Rarity.SUPER_RARE, 8.2, "9-sided ratchet, 6.0mm height"),
    ],
    "bits": [
        BeybladePart("Flat", PartType.BIT, "Standard", Rarity.COMMON, 2.1, "Aggressive attack bit with flat tip"),
        BeybladePart("Point", PartType.BIT, "Standard", Rarity.COMMON, 2.3, "Stamina bit with sharp point"),
        BeybladePart("Ball", PartType.BIT, "Standard", Rarity.COMMON, 2.5, "Defense bit with ball tip"),
        BeybladePart("Orb", PartType.BIT, "Standard", Rarity.COMMON, 2.4, "Balance bit with orb tip"),
        BeybladePart("Needle", PartType.BIT, "Standard", Rarity.RARE, 2.2, "High stamina bit with needle tip"),
        BeybladePart("Rush", PartType.BIT, "Standard", Rarity.RARE, 2.6, "High-speed attack bit"),
        BeybladePart("Taper", PartType.BIT, "Standard", Rarity.RARE, 2.4, "Balance bit with tapered tip"),
        BeybladePart("High Taper", PartType.BIT, "Special", Rarity.SUPER_RARE, 2.7, "Elevated taper bit for unique movement"),
        BeybladePart("Low Flat", PartType.BIT, "Special", Rarity.SUPER_RARE, 2.0, "Low-profile flat bit for aggressive attack"),
        BeybladePart("Gear Ball", PartType.BIT, "Special", Rarity.ULTRA_RARE, 3.1, "Motorized ball bit with gear mechanism"),
    ]
}

class Collection:
    def __init__(self):
        self.parts: List[BeybladePart] = []
        self.combos: List[BeybladeCombo] = []
    
    def add_part(self, part: BeybladePart):
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
    
    def save_to_file(self, filename: str):
        data = {
            'parts': [part.to_dict() for part in self.parts],
            'combos': [combo.to_dict() for combo in self.combos]
        }
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_from_file(self, filename: str):
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.parts = [BeybladePart.from_dict(part_data) for part_data in data.get('parts', [])]
            self.combos = [BeybladeCombo.from_dict(combo_data) for combo_data in data.get('combos', [])]
        except (FileNotFoundError, json.JSONDecodeError):
            pass

class BeybladeXManager:
    def __init__(self):
        try:
            logging.info("Starting Beyblade X Manager...")
            self.root = tk.Tk()
            self.root.title("🌪️ Beyblade X Collection Manager")
            self.root.geometry("1000x700")
            self.root.configure(bg='#2c3e50')
            
            logging.info("Loading collection...")
            self.collection = Collection()
            self.collection.load_from_file("collection.json")
            
            logging.info("Setting up UI...")
            self.setup_ui()
            logging.info("UI setup complete!")
            
        except Exception as e:
            logging.error(f"Error in __init__: {e}")
            messagebox.showerror("Initialization Error", f"Failed to start application: {e}")
            raise
        
    def setup_ui(self):
        # Main title
        title_label = tk.Label(self.root, text="🌪️ BEYBLADE X COLLECTION MANAGER 🌪️", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_collection_tab()
        self.create_database_tab()
        self.create_combos_tab()
        self.create_stats_tab()
        
        # Bottom frame for save button
        bottom_frame = tk.Frame(self.root, bg='#2c3e50')
        bottom_frame.pack(fill='x', padx=10, pady=5)
        
        save_btn = tk.Button(bottom_frame, text="💾 Save Collection", 
                            command=self.save_collection, font=('Arial', 10, 'bold'),
                            bg='#27ae60', fg='white', relief='raised')
        save_btn.pack(side='right', padx=5)
        
    def create_collection_tab(self):
        collection_frame = ttk.Frame(self.notebook)
        self.notebook.add(collection_frame, text="📦 My Collection")
        
        # Buttons frame
        btn_frame = tk.Frame(collection_frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        add_btn = tk.Button(btn_frame, text="➕ Add Part", command=self.add_part_dialog,
                           bg='#3498db', fg='white', font=('Arial', 9, 'bold'))
        add_btn.pack(side='left', padx=5)
        
        remove_btn = tk.Button(btn_frame, text="➖ Remove Part", command=self.remove_part_dialog,
                              bg='#e74c3c', fg='white', font=('Arial', 9, 'bold'))
        remove_btn.pack(side='left', padx=5)
        
        # Collection treeview
        self.collection_tree = ttk.Treeview(collection_frame, columns=('Type', 'Series', 'Rarity', 'Quantity', 'Condition'), show='tree headings')
        self.collection_tree.heading('#0', text='Part Name')
        self.collection_tree.heading('Type', text='Type')
        self.collection_tree.heading('Series', text='Series')
        self.collection_tree.heading('Rarity', text='Rarity')
        self.collection_tree.heading('Quantity', text='Owned')
        self.collection_tree.heading('Condition', text='Condition')
        
        self.collection_tree.column('#0', width=200)
        self.collection_tree.column('Type', width=80)
        self.collection_tree.column('Series', width=100)
        self.collection_tree.column('Rarity', width=100)
        self.collection_tree.column('Quantity', width=60)
        self.collection_tree.column('Condition', width=80)
        
        scrollbar1 = ttk.Scrollbar(collection_frame, orient='vertical', command=self.collection_tree.yview)
        self.collection_tree.configure(yscrollcommand=scrollbar1.set)
        
        self.collection_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=5)
        scrollbar1.pack(side='right', fill='y', pady=5)
        
        self.refresh_collection_view()
        
    def create_database_tab(self):
        database_frame = ttk.Frame(self.notebook)
        self.notebook.add(database_frame, text="🗃️ Database")
        
        # Search frame
        search_frame = tk.Frame(database_frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Search Database:", font=('Arial', 10)).pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_database)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Filter frame
        filter_frame = tk.Frame(database_frame)
        filter_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(filter_frame, text="Filter by Type:", font=('Arial', 10)).pack(side='left', padx=5)
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(filter_frame, textvariable=self.filter_var, 
                                   values=["All", "Blade", "Ratchet", "Bit"], state="readonly")
        filter_combo.pack(side='left', padx=5)
        filter_combo.bind('<<ComboboxSelected>>', self.filter_database)
        
        # Add to collection button
        add_to_collection_btn = tk.Button(filter_frame, text="➕ Add to Collection", 
                                         command=self.add_from_database,
                                         bg='#2ecc71', fg='white', font=('Arial', 9, 'bold'))
        add_to_collection_btn.pack(side='right', padx=5)
        
        # Database treeview
        self.database_tree = ttk.Treeview(database_frame, columns=('Type', 'Series', 'Rarity', 'Weight', 'Description'), show='tree headings')
        self.database_tree.heading('#0', text='Part Name')
        self.database_tree.heading('Type', text='Type')
        self.database_tree.heading('Series', text='Series')
        self.database_tree.heading('Rarity', text='Rarity')
        self.database_tree.heading('Weight', text='Weight (g)')
        self.database_tree.heading('Description', text='Description')
        
        self.database_tree.column('#0', width=150)
        self.database_tree.column('Type', width=80)
        self.database_tree.column('Series', width=80)
        self.database_tree.column('Rarity', width=100)
        self.database_tree.column('Weight', width=80)
        self.database_tree.column('Description', width=300)
        
        scrollbar2 = ttk.Scrollbar(database_frame, orient='vertical', command=self.database_tree.yview)
        self.database_tree.configure(yscrollcommand=scrollbar2.set)
        
        self.database_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=5)
        scrollbar2.pack(side='right', fill='y', pady=5)
        
        self.refresh_database_view()
        
    def create_combos_tab(self):
        combos_frame = ttk.Frame(self.notebook)
        self.notebook.add(combos_frame, text="⚔️ Combos")
        
        # Buttons frame
        combo_btn_frame = tk.Frame(combos_frame)
        combo_btn_frame.pack(fill='x', padx=10, pady=5)
        
        create_combo_btn = tk.Button(combo_btn_frame, text="🔧 Create Combo", 
                                    command=self.create_combo_dialog,
                                    bg='#9b59b6', fg='white', font=('Arial', 9, 'bold'))
        create_combo_btn.pack(side='left', padx=5)
        
        delete_combo_btn = tk.Button(combo_btn_frame, text="🗑️ Delete Combo", 
                                    command=self.delete_combo,
                                    bg='#e74c3c', fg='white', font=('Arial', 9, 'bold'))
        delete_combo_btn.pack(side='left', padx=5)
        
        # Combos treeview
        self.combos_tree = ttk.Treeview(combos_frame, columns=('Blade', 'Ratchet', 'Bit', 'Notes'), show='tree headings')
        self.combos_tree.heading('#0', text='Combo Name')
        self.combos_tree.heading('Blade', text='Blade')
        self.combos_tree.heading('Ratchet', text='Ratchet')
        self.combos_tree.heading('Bit', text='Bit')
        self.combos_tree.heading('Notes', text='Notes')
        
        self.combos_tree.column('#0', width=150)
        self.combos_tree.column('Blade', width=150)
        self.combos_tree.column('Ratchet', width=100)
        self.combos_tree.column('Bit', width=100)
        self.combos_tree.column('Notes', width=200)
        
        scrollbar3 = ttk.Scrollbar(combos_frame, orient='vertical', command=self.combos_tree.yview)
        self.combos_tree.configure(yscrollcommand=scrollbar3.set)
        
        self.combos_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=5)
        scrollbar3.pack(side='right', fill='y', pady=5)
        
        self.refresh_combos_view()
        
    def create_stats_tab(self):
        stats_frame = ttk.Frame(self.notebook)
        self.notebook.add(stats_frame, text="📊 Statistics")
        
        # Stats content
        stats_text = tk.Text(stats_frame, wrap=tk.WORD, font=('Arial', 10))
        stats_scrollbar = ttk.Scrollbar(stats_frame, orient='vertical', command=stats_text.yview)
        stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        stats_text.pack(side='left', fill='both', expand=True, padx=(10,0), pady=10)
        stats_scrollbar.pack(side='right', fill='y', pady=10)
        
        self.stats_text = stats_text
        self.refresh_stats()
        
    def refresh_collection_view(self):
        # Clear existing items
        for item in self.collection_tree.get_children():
            self.collection_tree.delete(item)
        
        # Add collection items
        for part in self.collection.parts:
            self.collection_tree.insert('', 'end', text=part.name,
                                       values=(part.part_type.value, part.series, 
                                              part.rarity.value, part.owned_quantity, part.condition))
    
    def refresh_database_view(self):
        # Clear existing items
        for item in self.database_tree.get_children():
            self.database_tree.delete(item)
        
        # Add database items based on current filter
        search_term = self.search_var.get().lower() if hasattr(self, 'search_var') else ""
        filter_type = self.filter_var.get() if hasattr(self, 'filter_var') else "All"
        
        all_parts = []
        all_parts.extend(BEYBLADE_X_DATABASE["blades"])
        all_parts.extend(BEYBLADE_X_DATABASE["ratchets"])
        all_parts.extend(BEYBLADE_X_DATABASE["bits"])
        
        for part in all_parts:
            # Apply filters
            if filter_type != "All" and part.part_type.value != filter_type:
                continue
            if search_term and search_term not in part.name.lower():
                continue
                
            self.database_tree.insert('', 'end', text=part.name,
                                     values=(part.part_type.value, part.series, 
                                            part.rarity.value, part.weight or "N/A", 
                                            part.description or ""))
    
    def refresh_combos_view(self):
        # Clear existing items
        for item in self.combos_tree.get_children():
            self.combos_tree.delete(item)
        
        # Add combo items
        for combo in self.collection.combos:
            self.combos_tree.insert('', 'end', text=combo.name,
                                   values=(combo.blade.name, combo.ratchet.name, 
                                          combo.bit.name, combo.notes or ""))
    
    def refresh_stats(self):
        if not hasattr(self, 'stats_text'):
            return
            
        self.stats_text.delete(1.0, tk.END)
        
        # Calculate statistics
        total_parts = len(self.collection.parts)
        total_quantity = sum(part.owned_quantity for part in self.collection.parts)
        
        blades = self.collection.get_parts_by_type(PartType.BLADE)
        ratchets = self.collection.get_parts_by_type(PartType.RATCHET)
        bits = self.collection.get_parts_by_type(PartType.BIT)
        
        # Rarity breakdown
        rarity_counts = {}
        for part in self.collection.parts:
            rarity = part.rarity.value
            rarity_counts[rarity] = rarity_counts.get(rarity, 0) + part.owned_quantity
        
        stats_content = f"""
🌪️ BEYBLADE X COLLECTION STATISTICS 🌪️

📦 COLLECTION OVERVIEW:
• Total Unique Parts: {total_parts}
• Total Parts Owned: {total_quantity}
• Total Combos Created: {len(self.collection.combos)}

🔧 PARTS BREAKDOWN:
• Blades: {len(blades)} unique ({sum(b.owned_quantity for b in blades)} total)
• Ratchets: {len(ratchets)} unique ({sum(r.owned_quantity for r in ratchets)} total)
• Bits: {len(bits)} unique ({sum(b.owned_quantity for b in bits)} total)

✨ RARITY BREAKDOWN:
"""
        
        for rarity, count in rarity_counts.items():
            stats_content += f"• {rarity}: {count} parts\n"
        
        if self.collection.parts:
            # Weight statistics
            parts_with_weight = [p for p in self.collection.parts if p.weight]
            if parts_with_weight:
                total_weight = sum(p.weight * p.owned_quantity for p in parts_with_weight)
                avg_weight = sum(p.weight for p in parts_with_weight) / len(parts_with_weight)
                
                stats_content += f"""
⚖️ WEIGHT STATISTICS:
• Total Collection Weight: {total_weight:.1f}g
• Average Part Weight: {avg_weight:.1f}g
"""
        
        # Most owned parts
        if self.collection.parts:
            most_owned = max(self.collection.parts, key=lambda p: p.owned_quantity)
            stats_content += f"""
🏆 COLLECTION HIGHLIGHTS:
• Most Owned Part: {most_owned.name} ({most_owned.owned_quantity} copies)
"""
        
        self.stats_text.insert(1.0, stats_content)
    
    def filter_database(self, *args):
        self.refresh_database_view()
    
    def add_part_dialog(self):
        dialog = AddPartDialog(self.root, BEYBLADE_X_DATABASE)
        if dialog.result:
            self.collection.add_part(dialog.result)
            self.refresh_collection_view()
            self.refresh_stats()
    
    def remove_part_dialog(self):
        selection = self.collection_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a part to remove.")
            return
        
        item = self.collection_tree.item(selection[0])
        part_name = item['text']
        part_type_str = item['values'][0]
        part_type = PartType(part_type_str)
        
        quantity = simpledialog.askinteger("Remove Part", 
                                          f"How many {part_name} to remove?", 
                                          minvalue=1)
        if quantity:
            if self.collection.remove_part(part_name, part_type, quantity):
                self.refresh_collection_view()
                self.refresh_stats()
                messagebox.showinfo("Success", f"Removed {quantity} {part_name}(s)")
            else:
                messagebox.showerror("Error", "Not enough parts to remove or part not found")
    
    def add_from_database(self):
        selection = self.database_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a part from the database.")
            return
        
        item = self.database_tree.item(selection[0])
        part_name = item['text']
        part_type_str = item['values'][0]
        part_type = PartType(part_type_str)
        
        # Find the part in database
        all_parts = []
        all_parts.extend(BEYBLADE_X_DATABASE["blades"])
        all_parts.extend(BEYBLADE_X_DATABASE["ratchets"])
        all_parts.extend(BEYBLADE_X_DATABASE["bits"])
        
        db_part = None
        for part in all_parts:
            if part.name == part_name and part.part_type == part_type:
                db_part = part
                break
        
        if db_part:
            quantity = simpledialog.askinteger("Add Part", 
                                              f"How many {part_name} to add?", 
                                              minvalue=1, initialvalue=1)
            if quantity:
                new_part = BeybladePart(
                    name=db_part.name,
                    part_type=db_part.part_type,
                    series=db_part.series,
                    rarity=db_part.rarity,
                    weight=db_part.weight,
                    description=db_part.description,
                    owned_quantity=quantity,
                    condition="New"
                )
                self.collection.add_part(new_part)
                self.refresh_collection_view()
                self.refresh_stats()
                messagebox.showinfo("Success", f"Added {quantity} {part_name}(s) to collection")
    
    def create_combo_dialog(self):
        dialog = CreateComboDialog(self.root, self.collection)
        if dialog.result:
            self.collection.combos.append(dialog.result)
            self.refresh_combos_view()
    
    def delete_combo(self):
        selection = self.combos_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a combo to delete.")
            return
        
        item = self.combos_tree.item(selection[0])
        combo_name = item['text']
        
        if messagebox.askyesno("Confirm Delete", f"Delete combo '{combo_name}'?"):
            # Find and remove the combo
            for i, combo in enumerate(self.collection.combos):
                if combo.name == combo_name:
                    del self.collection.combos[i]
                    break
            
            self.refresh_combos_view()
            messagebox.showinfo("Success", f"Deleted combo '{combo_name}'")
    
    def save_collection(self):
        try:
            self.collection.save_to_file("collection.json")
            messagebox.showinfo("Success", "Collection saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save collection: {e}")
    
    def run(self):
        """Start the application main loop"""
        try:
            logging.info("Entering main loop...")
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            messagebox.showerror("Runtime Error", f"Application error: {e}")

class AddPartDialog:
    def __init__(self, parent, database):
        self.result = None
        self.database = database
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Add Part to Collection")
        self.dialog.geometry("400x500")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_dialog()
        
    def setup_dialog(self):
        # Part type selection
        tk.Label(self.dialog, text="Part Type:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.part_type_var = tk.StringVar(value="Blade")
        part_type_frame = tk.Frame(self.dialog)
        part_type_frame.pack(pady=5)
        
        for part_type in ["Blade", "Ratchet", "Bit"]:
            tk.Radiobutton(part_type_frame, text=part_type, variable=self.part_type_var, 
                          value=part_type, command=self.update_part_list).pack(side='left', padx=10)
        
        # Part selection
        tk.Label(self.dialog, text="Select Part:", font=('Arial', 10, 'bold')).pack(pady=(20,5))
        self.part_listbox = tk.Listbox(self.dialog, height=10)
        self.part_listbox.pack(fill='both', expand=True, padx=20, pady=5)
        
        # Quantity
        tk.Label(self.dialog, text="Quantity:", font=('Arial', 10, 'bold')).pack(pady=(10,5))
        self.quantity_var = tk.IntVar(value=1)
        quantity_spinbox = tk.Spinbox(self.dialog, from_=1, to=99, textvariable=self.quantity_var, width=10)
        quantity_spinbox.pack(pady=5)
        
        # Condition
        tk.Label(self.dialog, text="Condition:", font=('Arial', 10, 'bold')).pack(pady=(10,5))
        self.condition_var = tk.StringVar(value="New")
        condition_combo = ttk.Combobox(self.dialog, textvariable=self.condition_var, 
                                      values=["New", "Like New", "Good", "Fair", "Poor"], 
                                      state="readonly", width=15)
        condition_combo.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Add", command=self.add_part, 
                 bg='#27ae60', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, 
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        
        self.update_part_list()
    
    def update_part_list(self):
        self.part_listbox.delete(0, tk.END)
        part_type = self.part_type_var.get().lower()
        
        if part_type == "blade":
            parts = self.database["blades"]
        elif part_type == "ratchet":
            parts = self.database["ratchets"]
        else:
            parts = self.database["bits"]
        
        for part in parts:
            self.part_listbox.insert(tk.END, f"{part.name} ({part.rarity.value})")
    
    def add_part(self):
        selection = self.part_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a part.")
            return
        
        part_type = self.part_type_var.get().lower()
        if part_type == "blade":
            parts = self.database["blades"]
        elif part_type == "ratchet":
            parts = self.database["ratchets"]
        else:
            parts = self.database["bits"]
        
        selected_part = parts[selection[0]]
        
        self.result = BeybladePart(
            name=selected_part.name,
            part_type=selected_part.part_type,
            series=selected_part.series,
            rarity=selected_part.rarity,
            weight=selected_part.weight,
            description=selected_part.description,
            owned_quantity=self.quantity_var.get(),
            condition=self.condition_var.get()
        )
        
        self.dialog.destroy()

class CreateComboDialog:
    def __init__(self, parent, collection):
        self.result = None
        self.collection = collection
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create Beyblade Combo")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))
        
        self.setup_dialog()
    
    def setup_dialog(self):
        # Combo name
        tk.Label(self.dialog, text="Combo Name:", font=('Arial', 10, 'bold')).pack(pady=5)
        self.name_var = tk.StringVar()
        tk.Entry(self.dialog, textvariable=self.name_var, width=30).pack(pady=5)
        
        # Part selections
        parts_frame = tk.Frame(self.dialog)
        parts_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Blade selection
        tk.Label(parts_frame, text="Blade:", font=('Arial', 10, 'bold')).grid(row=0, column=0, sticky='w', pady=5)
        self.blade_var = tk.StringVar()
        blade_combo = ttk.Combobox(parts_frame, textvariable=self.blade_var, state="readonly", width=25)
        blade_combo.grid(row=0, column=1, padx=10, pady=5)
        
        blades = self.collection.get_parts_by_type(PartType.BLADE)
        blade_combo['values'] = [f"{blade.name} (Qty: {blade.owned_quantity})" for blade in blades]
        
        # Ratchet selection
        tk.Label(parts_frame, text="Ratchet:", font=('Arial', 10, 'bold')).grid(row=1, column=0, sticky='w', pady=5)
        self.ratchet_var = tk.StringVar()
        ratchet_combo = ttk.Combobox(parts_frame, textvariable=self.ratchet_var, state="readonly", width=25)
        ratchet_combo.grid(row=1, column=1, padx=10, pady=5)
        
        ratchets = self.collection.get_parts_by_type(PartType.RATCHET)
        ratchet_combo['values'] = [f"{ratchet.name} (Qty: {ratchet.owned_quantity})" for ratchet in ratchets]
        
        # Bit selection
        tk.Label(parts_frame, text="Bit:", font=('Arial', 10, 'bold')).grid(row=2, column=0, sticky='w', pady=5)
        self.bit_var = tk.StringVar()
        bit_combo = ttk.Combobox(parts_frame, textvariable=self.bit_var, state="readonly", width=25)
        bit_combo.grid(row=2, column=1, padx=10, pady=5)
        
        bits = self.collection.get_parts_by_type(PartType.BIT)
        bit_combo['values'] = [f"{bit.name} (Qty: {bit.owned_quantity})" for bit in bits]
        
        # Notes
        tk.Label(self.dialog, text="Notes:", font=('Arial', 10, 'bold')).pack(pady=(20,5))
        self.notes_text = tk.Text(self.dialog, height=4, width=50)
        self.notes_text.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.dialog)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Create Combo", command=self.create_combo, 
                 bg='#9b59b6', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
        tk.Button(button_frame, text="Cancel", command=self.dialog.destroy, 
                 bg='#e74c3c', fg='white', font=('Arial', 10, 'bold')).pack(side='left', padx=10)
    
    def create_combo(self):
        if not all([self.name_var.get(), self.blade_var.get(), self.ratchet_var.get(), self.bit_var.get()]):
            messagebox.showwarning("Incomplete", "Please fill in all required fields.")
            return
        
        # Extract part names from combo box values
        blade_name = self.blade_var.get().split(" (Qty:")[0]
        ratchet_name = self.ratchet_var.get().split(" (Qty:")[0]
        bit_name = self.bit_var.get().split(" (Qty:")[0]
        
        # Find the actual parts
        blade = self.collection.find_part(blade_name, PartType.BLADE)
        ratchet = self.collection.find_part(ratchet_name, PartType.RATCHET)
        bit = self.collection.find_part(bit_name, PartType.BIT)
        
        if not all([blade, ratchet, bit]):
            messagebox.showerror("Error", "Could not find selected parts in collection.")
            return
        
        self.result = BeybladeCombo(
            name=self.name_var.get(),
            blade=blade,
            ratchet=ratchet,
            bit=bit,
            notes=self.notes_text.get(1.0, tk.END).strip() or None
        )
        
        self.dialog.destroy()

if __name__ == "__main__":
    try:
        logging.info("Application starting...")
        app = BeybladeXManager()
        logging.info("Starting main loop...")
        app.run()
    except Exception as e:
        logging.error(f"Fatal error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {e}")
        input("Press Enter to exit...")  # Keep console open to see error
