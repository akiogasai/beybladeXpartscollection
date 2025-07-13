"""Comprehensive Parts tab with all Beyblade X parts organized by category."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui.theme import BeybladeXTheme
from models import Collection, PartType, BeybladePart
from data.database import BEYBLADE_X_DATABASE


class PartsTab:
    """Comprehensive parts browser with all Beyblade X parts organized by category."""
    
    def __init__(self, parent_notebook, collection: Collection, refresh_callback):
        self.collection = collection
        self.refresh_callback = refresh_callback
        
        # Create main frame
        self.frame = BeybladeXTheme.create_frame(parent_notebook, 'background')
        parent_notebook.add(self.frame, text="🎯 All Parts")
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """Setup the parts browser UI."""
        main_container = BeybladeXTheme.create_frame(self.frame, 'background')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Header with search and quick actions
        self.create_header(main_container)
        
        # Main content - category tabs
        self.create_category_tabs(main_container)
    
    def create_header(self, parent):
        """Create header with search and quick actions."""
        header_card = BeybladeXTheme.create_card_frame(parent)
        header_card.pack(fill='x', pady=(0, 20))
        
        header_content = BeybladeXTheme.create_frame(header_card, 'surface')
        header_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Title and search row
        title_row = BeybladeXTheme.create_frame(header_content, 'surface')
        title_row.pack(fill='x', pady=(0, 10))
        
        BeybladeXTheme.create_label(
            title_row,
            "🎯 All Beyblade X Parts",
            'heading_medium'
        ).pack(side='left')
        
        # Search controls
        search_frame = BeybladeXTheme.create_frame(title_row, 'surface')
        search_frame.pack(side='right')
        
        BeybladeXTheme.create_label(
            search_frame,
            "Search:",
            'body'
        ).pack(side='left', padx=(0, 5))
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=25)
        search_entry.pack(side='left')
        
        # Info row
        info_row = BeybladeXTheme.create_frame(header_content, 'surface')
        info_row.pack(fill='x')
        
        total_parts = sum(len(parts) for parts in BEYBLADE_X_DATABASE.values())
        info_text = f"Browse {total_parts} official Beyblade X parts • Click any part to add to your collection"
        
        BeybladeXTheme.create_label(
            info_row,
            info_text,
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(side='left')
        
        # Quick add button
        BeybladeXTheme.create_button(
            info_row,
            "⚡ Quick Add Multiple",
            'accent',
            command=self.quick_add_multiple
        ).pack(side='right')
    
    def create_category_tabs(self, parent):
        """Create category tabs for different part types."""
        # Category notebook
        self.category_notebook = ttk.Notebook(parent)
        self.category_notebook.pack(fill='both', expand=True)
        
        # Create tabs for each part type
        self.create_blades_tab()
        self.create_ratchets_tab()
        self.create_bits_tab()
        self.create_all_parts_tab()
    
    def create_blades_tab(self):
        """Create the Blades tab."""
        blades_frame = BeybladeXTheme.create_frame(self.category_notebook, 'background')
        self.category_notebook.add(blades_frame, text="🗡️ Blades")
        
        # Content frame
        content_frame = BeybladeXTheme.create_frame(blades_frame, 'background')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Stats header for blades
        stats_card = BeybladeXTheme.create_card_frame(content_frame)
        stats_card.pack(fill='x', pady=(0, 10))
        
        stats_content = BeybladeXTheme.create_frame(stats_card, 'surface')
        stats_content.pack(fill='x', padx=15, pady=10)
        
        blade_count = len(BEYBLADE_X_DATABASE["blades"])
        BeybladeXTheme.create_label(
            stats_content,
            f"🗡️ {blade_count} Blades Available • Attack, Defense, Stamina & Balance Types",
            'heading_small'
        ).pack()
        
        # Blades grid
        self.blades_tree = self.create_parts_treeview(content_frame, BEYBLADE_X_DATABASE["blades"])
    
    def create_ratchets_tab(self):
        """Create the Ratchets tab."""
        ratchets_frame = BeybladeXTheme.create_frame(self.category_notebook, 'background')
        self.category_notebook.add(ratchets_frame, text="⚙️ Ratchets")
        
        content_frame = BeybladeXTheme.create_frame(ratchets_frame, 'background')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Stats header for ratchets
        stats_card = BeybladeXTheme.create_card_frame(content_frame)
        stats_card.pack(fill='x', pady=(0, 10))
        
        stats_content = BeybladeXTheme.create_frame(stats_card, 'surface')
        stats_content.pack(fill='x', padx=15, pady=10)
        
        ratchet_count = len(BEYBLADE_X_DATABASE["ratchets"])
        BeybladeXTheme.create_label(
            stats_content,
            f"⚙️ {ratchet_count} Ratchets Available • 60mm, 70mm, 80mm Heights • 1-10 Sided",
            'heading_small'
        ).pack()
        
        # Ratchets grid
        self.ratchets_tree = self.create_parts_treeview(content_frame, BEYBLADE_X_DATABASE["ratchets"])
    
    def create_bits_tab(self):
        """Create the Bits tab."""
        bits_frame = BeybladeXTheme.create_frame(self.category_notebook, 'background')
        self.category_notebook.add(bits_frame, text="🎯 Bits")
        
        content_frame = BeybladeXTheme.create_frame(bits_frame, 'background')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Stats header for bits
        stats_card = BeybladeXTheme.create_card_frame(content_frame)
        stats_card.pack(fill='x', pady=(0, 10))
        
        stats_content = BeybladeXTheme.create_frame(stats_card, 'surface')
        stats_content.pack(fill='x', padx=15, pady=10)
        
        bit_count = len(BEYBLADE_X_DATABASE["bits"])
        BeybladeXTheme.create_label(
            stats_content,
            f"🎯 {bit_count} Bits Available • Attack, Stamina, Defense, Balance & Special Types",
            'heading_small'
        ).pack()
        
        # Bits grid
        self.bits_tree = self.create_parts_treeview(content_frame, BEYBLADE_X_DATABASE["bits"])
    
    def create_all_parts_tab(self):
        """Create the All Parts tab."""
        all_frame = BeybladeXTheme.create_frame(self.category_notebook, 'background')
        self.category_notebook.add(all_frame, text="📋 All Parts")
        
        content_frame = BeybladeXTheme.create_frame(all_frame, 'background')
        content_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # All parts combined
        from data.database import get_all_parts
        all_parts = get_all_parts()
        self.all_parts_tree = self.create_parts_treeview(content_frame, all_parts)
    
    def create_parts_treeview(self, parent, parts_list):
        """Create a treeview for displaying parts."""
        # Treeview frame
        tree_card = BeybladeXTheme.create_card_frame(parent)
        tree_card.pack(fill='both', expand=True)
        
        # Treeview
        columns = ('Type', 'Series', 'Rarity', 'Weight', 'Description')
        tree = ttk.Treeview(tree_card, columns=columns, show='tree headings')
        
        # Configure columns
        tree.heading('#0', text='Part Name')
        tree.heading('Type', text='Type')
        tree.heading('Series', text='Series')
        tree.heading('Rarity', text='Rarity')
        tree.heading('Weight', text='Weight (g)')
        tree.heading('Description', text='Description')
        
        tree.column('#0', width=180)
        tree.column('Type', width=80)
        tree.column('Series', width=100)
        tree.column('Rarity', width=100)
        tree.column('Weight', width=80)
        tree.column('Description', width=300)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_card, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # Populate with parts
        for part in parts_list:
            # Color code by rarity
            tags = [part.rarity.value.lower().replace(' ', '_')]
            tree.insert('', 'end', text=part.name, tags=tags,
                       values=(part.part_type.value, part.series, part.rarity.value,
                             f"{part.weight:.1f}" if part.weight else "N/A", part.description or ""))
        
        # Configure rarity colors
        tree.tag_configure('common', background='#E8F5E8')
        tree.tag_configure('rare', background='#E8F0FF')
        tree.tag_configure('super_rare', background='#FFF0E8')
        tree.tag_configure('ultra_rare', background='#F8E8FF')
        
        # Bind click events
        tree.bind('<Double-1>', lambda e: self.add_part_to_collection(tree))
        tree.bind('<Button-1>', lambda e: self.on_single_click(tree, e))
        
        return tree
    
    def on_single_click(self, tree, event):
        """Handle single click to show part details."""
        selection = tree.selection()
        if selection:
            item = tree.item(selection[0])
            part_name = item['text']
            values = item['values']
            
            # Show tooltip or status update
            status_text = f"Click to add '{part_name}' to collection • Rarity: {values[2]} • Weight: {values[3]}g"
            # You could update a status bar here if you had one
    
    def add_part_to_collection(self, tree):
        """Add selected part to collection."""
        selection = tree.selection()
        if not selection:
            return
        
        item = tree.item(selection[0])
        part_name = item['text']
        part_type_str = item['values'][0]
        part_type = PartType(part_type_str)
        
        # Find the part in database
        from data.database import find_database_part
        db_part = find_database_part(part_name, part_type)
        
        if db_part:
            # Quick add dialog
            dialog = QuickAddPartDialog(self.frame, db_part, self.collection, self.refresh_callback)
    
    def quick_add_multiple(self):
        """Show dialog for adding multiple parts at once."""
        dialog = QuickAddMultipleDialog(self.frame, self.collection, self.refresh_callback)
    
    def on_search_change(self, *args):
        """Handle search text change."""
        search_term = self.search_var.get().lower()
        
        # Update all treeviews based on search
        if hasattr(self, 'blades_tree'):
            self.filter_treeview(self.blades_tree, BEYBLADE_X_DATABASE["blades"], search_term)
        if hasattr(self, 'ratchets_tree'):
            self.filter_treeview(self.ratchets_tree, BEYBLADE_X_DATABASE["ratchets"], search_term)
        if hasattr(self, 'bits_tree'):
            self.filter_treeview(self.bits_tree, BEYBLADE_X_DATABASE["bits"], search_term)
        if hasattr(self, 'all_parts_tree'):
            from data.database import get_all_parts
            self.filter_treeview(self.all_parts_tree, get_all_parts(), search_term)
    
    def filter_treeview(self, tree, parts_list, search_term):
        """Filter treeview based on search term."""
        # Clear existing items
        for item in tree.get_children():
            tree.delete(item)
        
        # Add filtered parts
        for part in parts_list:
            if not search_term or search_term in part.name.lower() or search_term in part.description.lower():
                tags = [part.rarity.value.lower().replace(' ', '_')]
                tree.insert('', 'end', text=part.name, tags=tags,
                           values=(part.part_type.value, part.series, part.rarity.value,
                                 f"{part.weight:.1f}" if part.weight else "N/A", part.description or ""))
    
    def refresh(self):
        """Refresh the parts display."""
        # Clear search
        self.search_var.set("")
        
        # Refresh all treeviews
        if hasattr(self, 'blades_tree'):
            self.filter_treeview(self.blades_tree, BEYBLADE_X_DATABASE["blades"], "")
        if hasattr(self, 'ratchets_tree'):
            self.filter_treeview(self.ratchets_tree, BEYBLADE_X_DATABASE["ratchets"], "")
        if hasattr(self, 'bits_tree'):
            self.filter_treeview(self.bits_tree, BEYBLADE_X_DATABASE["bits"], "")
        if hasattr(self, 'all_parts_tree'):
            from data.database import get_all_parts
            self.filter_treeview(self.all_parts_tree, get_all_parts(), "")


class QuickAddPartDialog:
    """Quick dialog for adding a single part to collection."""
    
    def __init__(self, parent, part: BeybladePart, collection: Collection, refresh_callback):
        self.part = part
        self.collection = collection
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Add {part.name}")
        self.dialog.geometry("400x300")
        self.dialog.configure(bg=BeybladeXTheme.COLORS['background'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 200, parent.winfo_rooty() + 100))
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the quick add dialog."""
        main_frame = BeybladeXTheme.create_frame(self.dialog, 'background')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Part info card
        info_card = BeybladeXTheme.create_card_frame(main_frame)
        info_card.pack(fill='x', pady=(0, 20))
        
        info_content = BeybladeXTheme.create_frame(info_card, 'surface')
        info_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Part details
        BeybladeXTheme.create_label(
            info_content,
            f"🎯 {self.part.name}",
            'heading_medium'
        ).pack(anchor='w')
        
        BeybladeXTheme.create_label(
            info_content,
            f"Type: {self.part.part_type.value} • Series: {self.part.series}",
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(anchor='w', pady=(5, 0))
        
        BeybladeXTheme.create_label(
            info_content,
            f"Rarity: {self.part.rarity.value} • Weight: {self.part.weight}g",
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(anchor='w')
        
        if self.part.description:
            BeybladeXTheme.create_label(
                info_content,
                self.part.description,
                'body_small',
                fg=BeybladeXTheme.COLORS['text_secondary']
            ).pack(anchor='w', pady=(10, 0))
        
        # Add options
        options_frame = BeybladeXTheme.create_frame(main_frame, 'background')
        options_frame.pack(fill='x', pady=(0, 20))
        
        # Quantity
        qty_frame = BeybladeXTheme.create_frame(options_frame, 'background')
        qty_frame.pack(anchor='w', pady=(0, 10))
        
        BeybladeXTheme.create_label(
            qty_frame,
            "Quantity:",
            'body'
        ).pack(side='left')
        
        self.quantity_var = tk.IntVar(value=1)
        qty_spinbox = tk.Spinbox(qty_frame, from_=1, to=99, textvariable=self.quantity_var, width=10)
        qty_spinbox.pack(side='left', padx=(10, 0))
        
        # Condition
        condition_frame = BeybladeXTheme.create_frame(options_frame, 'background')
        condition_frame.pack(anchor='w')
        
        BeybladeXTheme.create_label(
            condition_frame,
            "Condition:",
            'body'
        ).pack(side='left')
        
        self.condition_var = tk.StringVar(value="New")
        condition_combo = ttk.Combobox(
            condition_frame,
            textvariable=self.condition_var,
            values=["New", "Like New", "Good", "Fair", "Poor"],
            state="readonly",
            width=12
        )
        condition_combo.pack(side='left', padx=(10, 0))
        
        # Buttons
        button_frame = BeybladeXTheme.create_frame(main_frame, 'background')
        button_frame.pack(fill='x')
        
        BeybladeXTheme.create_button(
            button_frame,
            "➕ Add to Collection",
            'primary',
            command=self.add_part
        ).pack(side='right', padx=(10, 0))
        
        BeybladeXTheme.create_button(
            button_frame,
            "Cancel",
            'secondary',
            command=self.dialog.destroy
        ).pack(side='right')
    
    def add_part(self):
        """Add the part to collection."""
        new_part = BeybladePart(
            name=self.part.name,
            part_type=self.part.part_type,
            series=self.part.series,
            rarity=self.part.rarity,
            weight=self.part.weight,
            description=self.part.description,
            owned_quantity=self.quantity_var.get(),
            condition=self.condition_var.get()
        )
        
        self.collection.add_part(new_part)
        self.refresh_callback()
        
        messagebox.showinfo("Success", f"Added {self.quantity_var.get()} {self.part.name}(s) to your collection!")
        self.dialog.destroy()


class QuickAddMultipleDialog:
    """Dialog for adding multiple parts at once."""
    
    def __init__(self, parent, collection: Collection, refresh_callback):
        self.collection = collection
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Quick Add Multiple Parts")
        self.dialog.geometry("600x500")
        self.dialog.configure(bg=BeybladeXTheme.COLORS['background'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 50))
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the multiple add dialog."""
        main_frame = BeybladeXTheme.create_frame(self.dialog, 'background')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        BeybladeXTheme.create_label(
            main_frame,
            "⚡ Quick Add Multiple Parts",
            'heading_medium'
        ).pack(pady=(0, 20))
        
        # Quick sets
        sets_card = BeybladeXTheme.create_card_frame(main_frame)
        sets_card.pack(fill='x', pady=(0, 20))
        
        sets_content = BeybladeXTheme.create_frame(sets_card, 'surface')
        sets_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        BeybladeXTheme.create_label(
            sets_content,
            "Quick Starter Sets:",
            'heading_small'
        ).pack(anchor='w', pady=(0, 10))
        
        # Starter set buttons
        BeybladeXTheme.create_button(
            sets_content,
            "🎯 Basic Starter Set (Dran Sword + 3-60 + Flat)",
            'primary',
            command=self.add_basic_starter
        ).pack(fill='x', pady=2)
        
        BeybladeXTheme.create_button(
            sets_content,
            "⚔️ Complete Battle Set (5 Blades + 5 Ratchets + 5 Bits)",
            'accent',
            command=self.add_battle_set
        ).pack(fill='x', pady=2)
        
        BeybladeXTheme.create_button(
            sets_content,
            "🌟 All Common Parts",
            'secondary',
            command=self.add_all_common
        ).pack(fill='x', pady=2)
        
        # Custom selection (placeholder)
        custom_card = BeybladeXTheme.create_card_frame(main_frame)
        custom_card.pack(fill='both', expand=True)
        
        custom_content = BeybladeXTheme.create_frame(custom_card, 'surface')
        custom_content.pack(fill='both', expand=True, padx=15, pady=15)
        
        BeybladeXTheme.create_label(
            custom_content,
            "Custom selection interface coming soon!",
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(expand=True)
        
        # Close button
        BeybladeXTheme.create_button(
            main_frame,
            "Close",
            'secondary',
            command=self.dialog.destroy
        ).pack(pady=(20, 0))
    
    def add_basic_starter(self):
        """Add basic starter set."""
        from data.database import find_database_part
        
        parts_to_add = [
            ("Dran Sword", PartType.BLADE),
            ("3-60", PartType.RATCHET),
            ("Flat", PartType.BIT)
        ]
        
        added_count = 0
        for part_name, part_type in parts_to_add:
            db_part = find_database_part(part_name, part_type)
            if db_part:
                new_part = BeybladePart(
                    name=db_part.name,
                    part_type=db_part.part_type,
                    series=db_part.series,
                    rarity=db_part.rarity,
                    weight=db_part.weight,
                    description=db_part.description,
                    owned_quantity=1,
                    condition="New"
                )
                self.collection.add_part(new_part)
                added_count += 1
        
        self.refresh_callback()
        messagebox.showinfo("Success", f"Added {added_count} parts from Basic Starter Set!")
    
    def add_battle_set(self):
        """Add complete battle set."""
        from data.database import BEYBLADE_X_DATABASE
        
        added_count = 0
        
        # Add first 5 blades
        for blade in BEYBLADE_X_DATABASE["blades"][:5]:
            new_part = BeybladePart(
                name=blade.name,
                part_type=blade.part_type,
                series=blade.series,
                rarity=blade.rarity,
                weight=blade.weight,
                description=blade.description,
                owned_quantity=1,
                condition="New"
            )
            self.collection.add_part(new_part)
            added_count += 1
        
        # Add first 5 ratchets
        for ratchet in BEYBLADE_X_DATABASE["ratchets"][:5]:
            new_part = BeybladePart(
                name=ratchet.name,
                part_type=ratchet.part_type,
                series=ratchet.series,
                rarity=ratchet.rarity,
                weight=ratchet.weight,
                description=ratchet.description,
                owned_quantity=1,
                condition="New"
            )
            self.collection.add_part(new_part)
            added_count += 1
        
        # Add first 5 bits
        for bit in BEYBLADE_X_DATABASE["bits"][:5]:
            new_part = BeybladePart(
                name=bit.name,
                part_type=bit.part_type,
                series=bit.series,
                rarity=bit.rarity,
                weight=bit.weight,
                description=bit.description,
                owned_quantity=1,
                condition="New"
            )
            self.collection.add_part(new_part)
            added_count += 1
        
        self.refresh_callback()
        messagebox.showinfo("Success", f"Added {added_count} parts from Complete Battle Set!")
    
    def add_all_common(self):
        """Add all common rarity parts."""
        from data.database import get_all_parts
        from models.enums import Rarity
        
        all_parts = get_all_parts()
        added_count = 0
        
        for part in all_parts:
            if part.rarity == Rarity.COMMON:
                new_part = BeybladePart(
                    name=part.name,
                    part_type=part.part_type,
                    series=part.series,
                    rarity=part.rarity,
                    weight=part.weight,
                    description=part.description,
                    owned_quantity=1,
                    condition="New"
                )
                self.collection.add_part(new_part)
                added_count += 1
        
        self.refresh_callback()
        messagebox.showinfo("Success", f"Added {added_count} common parts to your collection!")
