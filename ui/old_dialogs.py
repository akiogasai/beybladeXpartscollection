"""Dialog windows for the Beyblade X Collection Manager."""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List
from models.part import BeybladePart
from models.combo import BeybladeCombo
from models.enums import PartType
from models.collection import Collection


class AddPartDialog:
    """Dialog for adding a part to the collection."""
    
    def __init__(self, parent, database: Dict):
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
        """Setup the dialog UI components."""
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
        """Update the part list based on selected type."""
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
        """Add the selected part to collection."""
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
    """Dialog for creating a new Beyblade combo."""
    
    def __init__(self, parent, collection: Collection):
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
        """Setup the dialog UI components."""
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
        """Create the combo with selected parts."""
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
