"""Collection tab for managing user's owned parts."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui.base_tab import BaseTab
from models.enums import PartType
from services.part_service import PartService


class CollectionTab(BaseTab):
    """Tab for viewing and managing the user's collection."""
    
    def __init__(self, parent_notebook, part_service: PartService):
        self.part_service = part_service
        super().__init__(parent_notebook, "📦 My Collection")
    
    def setup_ui(self):
        """Setup the collection tab UI."""
        # Buttons frame
        btn_frame = tk.Frame(self.frame)
        btn_frame.pack(fill='x', padx=10, pady=5)
        
        add_btn = tk.Button(btn_frame, text="➕ Add Part", command=self.add_part_dialog,
                           bg='#3498db', fg='white', font=('Arial', 9, 'bold'))
        add_btn.pack(side='left', padx=5)
        
        remove_btn = tk.Button(btn_frame, text="➖ Remove Part", command=self.remove_part_dialog,
                              bg='#e74c3c', fg='white', font=('Arial', 9, 'bold'))
        remove_btn.pack(side='left', padx=5)
        
        # Collection treeview
        columns = ('Type', 'Series', 'Rarity', 'Quantity', 'Condition')
        headings = {
            '#0': 'Part Name',
            'Type': 'Type',
            'Series': 'Series',
            'Rarity': 'Rarity',
            'Quantity': 'Owned',
            'Condition': 'Condition'
        }
        column_widths = {
            '#0': 200,
            'Type': 80,
            'Series': 100,
            'Rarity': 100,
            'Quantity': 60,
            'Condition': 80
        }
        
        self.collection_tree, self.scrollbar = self.create_treeview(columns, headings, column_widths)
        
        self.collection_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=5)
        self.scrollbar.pack(side='right', fill='y', pady=5)
        
        self.refresh()
    
    def refresh(self):
        """Refresh the collection view."""
        self.clear_treeview(self.collection_tree)
        
        collection = self.part_service.get_collection()
        for part in collection.parts:
            self.collection_tree.insert('', 'end', text=part.name,
                                       values=(part.part_type.value, part.series, 
                                              part.rarity.value, part.owned_quantity, part.condition))
    
    def add_part_dialog(self):
        """Show dialog to add a part to collection."""
        from ui.dialogs import AddPartDialog
        
        dialog = AddPartDialog(self.frame, self.part_service.get_database())
        if dialog.result:
            collection = self.part_service.get_collection()
            collection.add_part(dialog.result)
            self.refresh()
    
    def remove_part_dialog(self):
        """Show dialog to remove a part from collection."""
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
            collection = self.part_service.get_collection()
            if collection.remove_part(part_name, part_type, quantity):
                self.refresh()
                messagebox.showinfo("Success", f"Removed {quantity} {part_name}(s)")
            else:
                messagebox.showerror("Error", "Not enough parts to remove or part not found")
