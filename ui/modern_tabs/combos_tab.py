"""Modern combos tab with streamlined combo management."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui.theme import BeybladeXTheme
from models import Collection, BeybladeCombo, PartType


class CombosTab:
    """Modern combos tab with improved combo creation and management."""
    
    def __init__(self, parent_notebook, collection: Collection, refresh_callback):
        self.collection = collection
        self.refresh_callback = refresh_callback
        
        # Create main frame
        self.frame = BeybladeXTheme.create_frame(parent_notebook, 'background')
        parent_notebook.add(self.frame, text="⚔️ Combos")
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """Setup the combos tab UI."""
        main_container = BeybladeXTheme.create_frame(self.frame, 'background')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with title and actions
        self.create_header(main_container)
        
        # Main content area
        self.create_main_content(main_container)
        
        # Check if user has parts to create combos
        if not self.can_create_combos():
            self.show_no_parts_message(main_container)
    
    def create_header(self, parent):
        """Create header section."""
        header_card = BeybladeXTheme.create_card_frame(parent)
        header_card.pack(fill='x', pady=(0, 20))
        
        header_content = BeybladeXTheme.create_frame(header_card, 'surface')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Title row
        title_row = BeybladeXTheme.create_frame(header_content, 'surface')
        title_row.pack(fill='x')
        
        BeybladeXTheme.create_label(
            title_row,
            "⚔️ Battle Combos",
            'heading_medium'
        ).pack(side='left')
        
        # Action buttons
        buttons_frame = BeybladeXTheme.create_frame(title_row, 'surface')
        buttons_frame.pack(side='right')
        
        if self.can_create_combos():
            BeybladeXTheme.create_button(
                buttons_frame,
                "🔧 Create Combo",
                'primary',
                command=self.create_combo_dialog
            ).pack(side='right', padx=(10, 0))
        
        BeybladeXTheme.create_button(
            buttons_frame,
            "🗑️ Delete Selected",
            'danger',
            command=self.delete_selected_combo
        ).pack(side='right')
    
    def create_main_content(self, parent):
        """Create main content area."""
        if len(self.collection.combos) == 0:
            self.create_empty_state(parent)
        else:
            self.create_combos_list(parent)
    
    def create_empty_state(self, parent):
        """Create empty state when no combos exist."""
        empty_card = BeybladeXTheme.create_card_frame(parent)
        empty_card.pack(fill='both', expand=True)
        
        empty_content = BeybladeXTheme.create_frame(empty_card, 'surface')
        empty_content.pack(fill='both', expand=True, padx=40, pady=40)
        
        # Empty state icon and text
        BeybladeXTheme.create_label(
            empty_content,
            "⚔️",
            'heading_large'
        ).pack(pady=(0, 20))
        
        BeybladeXTheme.create_label(
            empty_content,
            "No Battle Combos Yet",
            'heading_medium'
        ).pack(pady=(0, 10))
        
        if self.can_create_combos():
            BeybladeXTheme.create_label(
                empty_content,
                "Create your first combo by combining parts from your collection!",
                'body',
                fg=BeybladeXTheme.COLORS['text_secondary']
            ).pack(pady=(0, 30))
            
            BeybladeXTheme.create_button(
                empty_content,
                "🔧 Create Your First Combo",
                'primary',
                command=self.create_combo_dialog
            ).pack()
        else:
            BeybladeXTheme.create_label(
                empty_content,
                "You need at least one Blade, Ratchet, and Bit in your collection to create combos.",
                'body',
                fg=BeybladeXTheme.COLORS['text_secondary']
            ).pack(pady=(0, 20))
            
            BeybladeXTheme.create_button(
                empty_content,
                "🎯 Browse All Parts",
                'secondary',
                command=self.go_to_parts_manager
            ).pack()
    
    def create_combos_list(self, parent):
        """Create the combos list view."""
        list_card = BeybladeXTheme.create_card_frame(parent)
        list_card.pack(fill='both', expand=True)
        
        # Combos treeview
        columns = ('Blade', 'Ratchet', 'Bit', 'Notes')
        self.combos_tree = ttk.Treeview(list_card, columns=columns, show='tree headings')
        
        # Configure columns
        self.combos_tree.heading('#0', text='Combo Name')
        self.combos_tree.heading('Blade', text='Blade')
        self.combos_tree.heading('Ratchet', text='Ratchet')
        self.combos_tree.heading('Bit', text='Bit')
        self.combos_tree.heading('Notes', text='Notes')
        
        self.combos_tree.column('#0', width=200)
        self.combos_tree.column('Blade', width=150)
        self.combos_tree.column('Ratchet', width=100)
        self.combos_tree.column('Bit', width=100)
        self.combos_tree.column('Notes', width=200)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_card, orient='vertical', command=self.combos_tree.yview)
        self.combos_tree.configure(yscrollcommand=scrollbar.set)
        
        self.combos_tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Double-click to edit
        self.combos_tree.bind('<Double-1>', self.edit_combo)
    
    def show_no_parts_message(self, parent):
        """Show message when user doesn't have enough parts."""
        if hasattr(self, 'combos_tree'):
            return  # Already showing combos list
        
        warning_card = BeybladeXTheme.create_card_frame(parent)
        warning_card.pack(fill='x', pady=(20, 0))
        
        warning_content = BeybladeXTheme.create_frame(warning_card, 'surface')
        warning_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        BeybladeXTheme.create_label(
            warning_content,
            "⚠️ Need More Parts",
            'heading_small',
            fg=BeybladeXTheme.COLORS['warning']
        ).pack(anchor='w')
        
        missing_parts = self.get_missing_parts()
        BeybladeXTheme.create_label(
            warning_content,
            f"To create combos, you need: {', '.join(missing_parts)}",
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(anchor='w', pady=(5, 0))
    
    def can_create_combos(self):
        """Check if user has enough parts to create combos."""
        blades = self.collection.get_parts_by_type(PartType.BLADE)
        ratchets = self.collection.get_parts_by_type(PartType.RATCHET)
        bits = self.collection.get_parts_by_type(PartType.BIT)
        
        return len(blades) > 0 and len(ratchets) > 0 and len(bits) > 0
    
    def get_missing_parts(self):
        """Get list of missing part types."""
        missing = []
        
        if len(self.collection.get_parts_by_type(PartType.BLADE)) == 0:
            missing.append("Blade")
        if len(self.collection.get_parts_by_type(PartType.RATCHET)) == 0:
            missing.append("Ratchet")
        if len(self.collection.get_parts_by_type(PartType.BIT)) == 0:
            missing.append("Bit")
        
        return missing
    
    def create_combo_dialog(self):
        """Show create combo dialog."""
        dialog = CreateComboDialog(self.frame, self.collection, self.refresh_callback)
    
    def delete_selected_combo(self):
        """Delete selected combo."""
        if not hasattr(self, 'combos_tree'):
            return
        
        selection = self.combos_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a combo to delete.")
            return
        
        item = self.combos_tree.item(selection[0])
        combo_name = item['text']
        
        if messagebox.askyesno("Confirm Delete", f"Delete combo '{combo_name}'?"):
            if self.collection.remove_combo(combo_name):
                self.refresh_callback()
                messagebox.showinfo("Success", f"Deleted combo '{combo_name}'")
            else:
                messagebox.showerror("Error", "Failed to delete combo")
    
    def edit_combo(self, event):
        """Edit selected combo (placeholder)."""
        selection = self.combos_tree.selection()
        if selection:
            messagebox.showinfo("Edit Combo", "Combo editing coming soon!")
    
    def go_to_parts_manager(self):
        """Switch to All Parts tab."""
        notebook = self.frame.master
        notebook.select(1)
    
    def refresh(self):
        """Refresh the combos view."""
        # Clear and recreate content
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.setup_ui()
        
        if hasattr(self, 'combos_tree'):
            # Refresh combos list
            for item in self.combos_tree.get_children():
                self.combos_tree.delete(item)
            
            for combo in self.collection.combos:
                self.combos_tree.insert('', 'end', text=combo.name,
                                       values=(combo.blade.name, combo.ratchet.name,
                                             combo.bit.name, combo.notes or ""))


class CreateComboDialog:
    """Modern create combo dialog."""
    
    def __init__(self, parent, collection: Collection, refresh_callback):
        self.collection = collection
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Create Battle Combo")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg=BeybladeXTheme.COLORS['background'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 50))
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the create combo dialog."""
        main_frame = BeybladeXTheme.create_frame(self.dialog, 'background')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        BeybladeXTheme.create_label(
            main_frame,
            "⚔️ Create Battle Combo",
            'heading_medium'
        ).pack(pady=(0, 20))
        
        # Content card
        content_card = BeybladeXTheme.create_card_frame(main_frame)
        content_card.pack(fill='both', expand=True, pady=(0, 20))
        
        content_frame = BeybladeXTheme.create_frame(content_card, 'surface')
        content_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Combo name
        name_frame = BeybladeXTheme.create_frame(content_frame, 'surface')
        name_frame.pack(fill='x', pady=(0, 20))
        
        BeybladeXTheme.create_label(
            name_frame,
            "Combo Name:",
            'heading_small'
        ).pack(anchor='w')
        
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(name_frame, textvariable=self.name_var, font=BeybladeXTheme.FONTS['body'])
        name_entry.pack(fill='x', pady=(5, 0))
        name_entry.focus()
        
        # Parts selection
        parts_frame = BeybladeXTheme.create_frame(content_frame, 'surface')
        parts_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Blade selection
        self.create_part_selector(parts_frame, "🗡️ Blade:", PartType.BLADE, 0)
        
        # Ratchet selection
        self.create_part_selector(parts_frame, "⚙️ Ratchet:", PartType.RATCHET, 1)
        
        # Bit selection
        self.create_part_selector(parts_frame, "🎯 Bit:", PartType.BIT, 2)
        
        # Notes
        notes_frame = BeybladeXTheme.create_frame(content_frame, 'surface')
        notes_frame.pack(fill='x', pady=(0, 20))
        
        BeybladeXTheme.create_label(
            notes_frame,
            "Notes (optional):",
            'heading_small'
        ).pack(anchor='w')
        
        self.notes_text = tk.Text(notes_frame, height=3, font=BeybladeXTheme.FONTS['body'])
        self.notes_text.pack(fill='x', pady=(5, 0))
        
        # Buttons
        button_frame = BeybladeXTheme.create_frame(main_frame, 'background')
        button_frame.pack(fill='x')
        
        BeybladeXTheme.create_button(
            button_frame,
            "⚔️ Create Combo",
            'primary',
            command=self.create_combo
        ).pack(side='right', padx=(10, 0))
        
        BeybladeXTheme.create_button(
            button_frame,
            "Cancel",
            'secondary',
            command=self.dialog.destroy
        ).pack(side='right')
    
    def create_part_selector(self, parent, label, part_type, row):
        """Create a part selector row."""
        BeybladeXTheme.create_label(
            parent,
            label,
            'body'
        ).grid(row=row, column=0, sticky='w', pady=5, padx=(0, 10))
        
        # Create variable for this part type
        if part_type == PartType.BLADE:
            self.blade_var = tk.StringVar()
            var = self.blade_var
        elif part_type == PartType.RATCHET:
            self.ratchet_var = tk.StringVar()
            var = self.ratchet_var
        else:  # BIT
            self.bit_var = tk.StringVar()
            var = self.bit_var
        
        # Get available parts
        parts = self.collection.get_parts_by_type(part_type)
        values = [f"{part.name} (Qty: {part.owned_quantity})" for part in parts]
        
        combo = ttk.Combobox(parent, textvariable=var, values=values, state="readonly", width=30)
        combo.grid(row=row, column=1, sticky='ew', pady=5)
        
        # Configure grid
        parent.grid_columnconfigure(1, weight=1)
    
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
        
        # Create combo
        combo = BeybladeCombo(
            name=self.name_var.get(),
            blade=blade,
            ratchet=ratchet,
            bit=bit,
            notes=self.notes_text.get(1.0, tk.END).strip() or None
        )
        
        self.collection.add_combo(combo)
        self.refresh_callback()
        
        messagebox.showinfo("Success", f"Created combo '{combo.name}'!")
        self.dialog.destroy()
