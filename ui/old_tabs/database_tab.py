"""Database tab for browsing available parts."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui.base_tab import BaseTab
from models.enums import PartType
from models.part import BeybladePart
from services.part_service import PartService


class DatabaseTab(BaseTab):
    """Tab for browsing the parts database."""
    
    def __init__(self, parent_notebook, part_service: PartService):
        self.part_service = part_service
        super().__init__(parent_notebook, "🗃️ Database")
    
    def setup_ui(self):
        """Setup the database tab UI."""
        # Search frame
        search_frame = tk.Frame(self.frame)
        search_frame.pack(fill='x', padx=10, pady=5)
        
        tk.Label(search_frame, text="Search Database:", font=('Arial', 10)).pack(side='left', padx=5)
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_database)
        search_entry = tk.Entry(search_frame, textvariable=self.search_var, width=30)
        search_entry.pack(side='left', padx=5)
        
        # Filter frame
        filter_frame = tk.Frame(self.frame)
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
        columns = ('Type', 'Series', 'Rarity', 'Weight', 'Description')
        headings = {
            '#0': 'Part Name',
            'Type': 'Type',
            'Series': 'Series',
            'Rarity': 'Rarity',
            'Weight': 'Weight (g)',
            'Description': 'Description'
        }
        column_widths = {
            '#0': 150,
            'Type': 80,
            'Series': 80,
            'Rarity': 100,
            'Weight': 80,
            'Description': 300
        }
        
        self.database_tree, self.scrollbar = self.create_treeview(columns, headings, column_widths)
        
        self.database_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=5)
        self.scrollbar.pack(side='right', fill='y', pady=5)
        
        self.refresh()
    
    def refresh(self):
        """Refresh the database view."""
        self.filter_database()
    
    def filter_database(self, *args):
        """Filter database based on search and type filters."""
        self.clear_treeview(self.database_tree)
        
        search_term = self.search_var.get().lower()
        filter_type = self.filter_var.get()
        
        database = self.part_service.get_database()
        all_parts = []
        all_parts.extend(database["blades"])
        all_parts.extend(database["ratchets"])
        all_parts.extend(database["bits"])
        
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
    
    def add_from_database(self):
        """Add selected part from database to collection."""
        selection = self.database_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a part from the database.")
            return
        
        item = self.database_tree.item(selection[0])
        part_name = item['text']
        part_type_str = item['values'][0]
        part_type = PartType(part_type_str)
        
        # Find the part in database
        database = self.part_service.get_database()
        all_parts = []
        all_parts.extend(database["blades"])
        all_parts.extend(database["ratchets"])
        all_parts.extend(database["bits"])
        
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
                collection = self.part_service.get_collection()
                collection.add_part(new_part)
                messagebox.showinfo("Success", f"Added {quantity} {part_name}(s) to collection")
