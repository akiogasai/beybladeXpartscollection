"""Combos tab for managing Beyblade combinations."""

import tkinter as tk
from tkinter import ttk, messagebox
from ui.base_tab import BaseTab
from services.part_service import PartService


class CombosTab(BaseTab):
    """Tab for creating and managing Beyblade combos."""
    
    def __init__(self, parent_notebook, part_service: PartService):
        self.part_service = part_service
        super().__init__(parent_notebook, "⚔️ Combos")
    
    def setup_ui(self):
        """Setup the combos tab UI."""
        # Buttons frame
        combo_btn_frame = tk.Frame(self.frame)
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
        columns = ('Blade', 'Ratchet', 'Bit', 'Notes')
        headings = {
            '#0': 'Combo Name',
            'Blade': 'Blade',
            'Ratchet': 'Ratchet',
            'Bit': 'Bit',
            'Notes': 'Notes'
        }
        column_widths = {
            '#0': 150,
            'Blade': 150,
            'Ratchet': 100,
            'Bit': 100,
            'Notes': 200
        }
        
        self.combos_tree, self.scrollbar = self.create_treeview(columns, headings, column_widths)
        
        self.combos_tree.pack(side='left', fill='both', expand=True, padx=(10,0), pady=5)
        self.scrollbar.pack(side='right', fill='y', pady=5)
        
        self.refresh()
    
    def refresh(self):
        """Refresh the combos view."""
        self.clear_treeview(self.combos_tree)
        
        collection = self.part_service.get_collection()
        for combo in collection.combos:
            self.combos_tree.insert('', 'end', text=combo.name,
                                   values=(combo.blade.name, combo.ratchet.name, 
                                          combo.bit.name, combo.notes or ""))
    
    def create_combo_dialog(self):
        """Show dialog to create a new combo."""
        from ui.dialogs import CreateComboDialog
        
        collection = self.part_service.get_collection()
        dialog = CreateComboDialog(self.frame, collection)
        if dialog.result:
            collection.combos.append(dialog.result)
            self.refresh()
    
    def delete_combo(self):
        """Delete selected combo."""
        selection = self.combos_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a combo to delete.")
            return
        
        item = self.combos_tree.item(selection[0])
        combo_name = item['text']
        
        if messagebox.askyesno("Confirm Delete", f"Delete combo '{combo_name}'?"):
            collection = self.part_service.get_collection()
            # Find and remove the combo
            for i, combo in enumerate(collection.combos):
                if combo.name == combo_name:
                    del collection.combos[i]
                    break
            
            self.refresh()
            messagebox.showinfo("Success", f"Deleted combo '{combo_name}'")
