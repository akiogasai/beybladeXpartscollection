"""Modern parts manager tab combining collection and database views."""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ui.theme import BeybladeXTheme
from models import Collection, PartType, BeybladePart
from services.part_service import PartService
from data.database import BEYBLADE_X_DATABASE, find_database_part


class PartsManagerTab:
    """Modern parts manager with integrated collection and database views."""
    
    def __init__(self, parent_notebook, collection: Collection, part_service: PartService, refresh_callback):
        self.collection = collection
        self.part_service = part_service
        self.refresh_callback = refresh_callback
        
        # Create main frame
        self.frame = BeybladeXTheme.create_frame(parent_notebook, 'background')
        parent_notebook.add(self.frame, text="🎯 Parts Manager")
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """Setup the parts manager UI."""
        # Main container with better layout
        main_container = BeybladeXTheme.create_frame(self.frame, 'background')
        main_container.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Top controls
        self.create_controls(main_container)
        
        # Main content area - split between database and collection
        self.create_main_content(main_container)
    
    def create_controls(self, parent):
        """Create top control panel with search and filters."""
        controls_card = BeybladeXTheme.create_card_frame(parent)
        controls_card.pack(fill='x', pady=(0, 20))
        
        controls_content = BeybladeXTheme.create_frame(controls_card, 'surface')
        controls_content.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Title and search row
        title_row = BeybladeXTheme.create_frame(controls_content, 'surface')
        title_row.pack(fill='x', pady=(0, 10))
        
        BeybladeXTheme.create_label(
            title_row,
            "Parts Manager",
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
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, width=20)
        search_entry.pack(side='left', padx=(0, 10))
        
        # Filter controls
        filter_frame = BeybladeXTheme.create_frame(controls_content, 'surface')
        filter_frame.pack(fill='x')
        
        BeybladeXTheme.create_label(
            filter_frame,
            "Filter by Type:",
            'body'
        ).pack(side='left', padx=(0, 5))
        
        self.filter_var = tk.StringVar(value="All")
        filter_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.filter_var,
            values=["All", "Blade", "Ratchet", "Bit"],
            state="readonly",
            width=12
        )
        filter_combo.pack(side='left', padx=(0, 20))
        filter_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # Quick add button
        BeybladeXTheme.create_button(
            filter_frame,
            "⚡ Quick Add",
            'primary',
            command=self.quick_add_dialog
        ).pack(side='right')
    
    def create_main_content(self, parent):
        """Create the main content area with database and collection views."""
        # Horizontal paned window for better layout
        paned_window = tk.PanedWindow(parent, orient=tk.HORIZONTAL, 
                                     bg=BeybladeXTheme.COLORS['background'],
                                     sashwidth=5, relief='flat')
        paned_window.pack(fill='both', expand=True)
        
        # Database panel (left)
        self.create_database_panel(paned_window)
        
        # Collection panel (right)
        self.create_collection_panel(paned_window)
        
        # Set initial sash position (60% database, 40% collection)
        paned_window.update_idletasks()
        paned_window.sash_place(0, int(paned_window.winfo_width() * 0.6), 0)
    
    def create_database_panel(self, parent):
        """Create the database browser panel."""
        db_card = BeybladeXTheme.create_card_frame(parent)
        parent.add(db_card)
        
        # Header
        header_frame = BeybladeXTheme.create_frame(db_card, 'primary')
        header_frame.pack(fill='x')
        
        BeybladeXTheme.create_label(
            header_frame,
            "🗃️ Parts Database",
            'heading_small',
            bg=BeybladeXTheme.COLORS['primary'],
            fg=BeybladeXTheme.COLORS['text_on_primary']
        ).pack(side='left', padx=15, pady=10)
        
        BeybladeXTheme.create_button(
            header_frame,
            "➕ Add to Collection",
            'success',
            command=self.add_selected_to_collection
        ).pack(side='right', padx=15, pady=5)
        
        # Database treeview
        db_frame = BeybladeXTheme.create_frame(db_card, 'surface')
        db_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        columns = ('Type', 'Series', 'Rarity', 'Weight')
        self.database_tree = ttk.Treeview(db_frame, columns=columns, show='tree headings', height=15)
        
        # Configure columns
        self.database_tree.heading('#0', text='Part Name')
        self.database_tree.heading('Type', text='Type')
        self.database_tree.heading('Series', text='Series')
        self.database_tree.heading('Rarity', text='Rarity')
        self.database_tree.heading('Weight', text='Weight (g)')
        
        self.database_tree.column('#0', width=180)
        self.database_tree.column('Type', width=80)
        self.database_tree.column('Series', width=80)
        self.database_tree.column('Rarity', width=100)
        self.database_tree.column('Weight', width=80)
        
        # Scrollbar for database
        db_scrollbar = ttk.Scrollbar(db_frame, orient='vertical', command=self.database_tree.yview)
        self.database_tree.configure(yscrollcommand=db_scrollbar.set)
        
        self.database_tree.pack(side='left', fill='both', expand=True)
        db_scrollbar.pack(side='right', fill='y')
        
        # Double-click to add
        self.database_tree.bind('<Double-1>', lambda e: self.add_selected_to_collection())
    
    def create_collection_panel(self, parent):
        """Create the collection view panel."""
        collection_card = BeybladeXTheme.create_card_frame(parent)
        parent.add(collection_card)
        
        # Header
        header_frame = BeybladeXTheme.create_frame(collection_card, 'accent')
        header_frame.pack(fill='x')
        
        BeybladeXTheme.create_label(
            header_frame,
            "📦 My Collection",
            'heading_small',
            bg=BeybladeXTheme.COLORS['accent'],
            fg=BeybladeXTheme.COLORS['text_on_primary']
        ).pack(side='left', padx=15, pady=10)
        
        BeybladeXTheme.create_button(
            header_frame,
            "➖ Remove Selected",
            'danger',
            command=self.remove_selected_from_collection
        ).pack(side='right', padx=15, pady=5)
        
        # Collection treeview
        collection_frame = BeybladeXTheme.create_frame(collection_card, 'surface')
        collection_frame.pack(fill='both', expand=True, padx=0, pady=0)
        
        columns = ('Type', 'Rarity', 'Quantity', 'Condition')
        self.collection_tree = ttk.Treeview(collection_frame, columns=columns, show='tree headings', height=15)
        
        # Configure columns
        self.collection_tree.heading('#0', text='Part Name')
        self.collection_tree.heading('Type', text='Type')
        self.collection_tree.heading('Rarity', text='Rarity')
        self.collection_tree.heading('Quantity', text='Owned')
        self.collection_tree.heading('Condition', text='Condition')
        
        self.collection_tree.column('#0', width=150)
        self.collection_tree.column('Type', width=80)
        self.collection_tree.column('Rarity', width=100)
        self.collection_tree.column('Quantity', width=60)
        self.collection_tree.column('Condition', width=80)
        
        # Scrollbar for collection
        collection_scrollbar = ttk.Scrollbar(collection_frame, orient='vertical', command=self.collection_tree.yview)
        self.collection_tree.configure(yscrollcommand=collection_scrollbar.set)
        
        self.collection_tree.pack(side='left', fill='both', expand=True)
        collection_scrollbar.pack(side='right', fill='y')
    
    def quick_add_dialog(self):
        """Show quick add dialog for adding parts."""
        dialog = QuickAddDialog(self.frame, self.collection, self.refresh_callback)
    
    def add_selected_to_collection(self):
        """Add selected database part to collection."""
        selection = self.database_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a part from the database.")
            return
        
        item = self.database_tree.item(selection[0])
        part_name = item['text']
        part_type_str = item['values'][0]
        part_type = PartType(part_type_str)
        
        # Find the part in database
        db_part = find_database_part(part_name, part_type)
        if db_part:
            quantity = simpledialog.askinteger(
                "Add Part",
                f"How many {part_name} to add?",
                minvalue=1,
                initialvalue=1
            )
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
                self.refresh_callback()
                messagebox.showinfo("Success", f"Added {quantity} {part_name}(s) to collection")
    
    def remove_selected_from_collection(self):
        """Remove selected part from collection."""
        selection = self.collection_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a part to remove.")
            return
        
        item = self.collection_tree.item(selection[0])
        part_name = item['text']
        part_type_str = item['values'][0]
        part_type = PartType(part_type_str)
        
        quantity = simpledialog.askinteger(
            "Remove Part",
            f"How many {part_name} to remove?",
            minvalue=1
        )
        if quantity:
            if self.collection.remove_part(part_name, part_type, quantity):
                self.refresh_callback()
                messagebox.showinfo("Success", f"Removed {quantity} {part_name}(s)")
            else:
                messagebox.showerror("Error", "Not enough parts to remove or part not found")
    
    def on_search_change(self, *args):
        """Handle search text change."""
        self.refresh_database_view()
    
    def on_filter_change(self, *args):
        """Handle filter change."""
        self.refresh_database_view()
    
    def refresh_database_view(self):
        """Refresh the database view with current filters."""
        # Clear existing items
        for item in self.database_tree.get_children():
            self.database_tree.delete(item)
        
        # Get all parts and apply filters
        from data.database import get_all_parts
        all_parts = get_all_parts()
        
        search_term = self.search_var.get().lower()
        filter_type = self.filter_var.get()
        
        for part in all_parts:
            # Apply filters
            if filter_type != "All" and part.part_type.value != filter_type:
                continue
            if search_term and search_term not in part.name.lower():
                continue
            
            self.database_tree.insert('', 'end', text=part.name,
                                     values=(part.part_type.value, part.series,
                                           part.rarity.value, part.weight or "N/A"))
    
    def refresh_collection_view(self):
        """Refresh the collection view."""
        # Clear existing items
        for item in self.collection_tree.get_children():
            self.collection_tree.delete(item)
        
        # Add collection items
        for part in self.collection.parts:
            self.collection_tree.insert('', 'end', text=part.name,
                                       values=(part.part_type.value, part.rarity.value,
                                             part.owned_quantity, part.condition))
    
    def refresh(self):
        """Refresh both database and collection views."""
        self.refresh_database_view()
        self.refresh_collection_view()


class QuickAddDialog:
    """Quick add dialog for adding multiple parts efficiently."""
    
    def __init__(self, parent, collection: Collection, refresh_callback):
        self.collection = collection
        self.refresh_callback = refresh_callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Quick Add Parts")
        self.dialog.geometry("500x400")
        self.dialog.configure(bg=BeybladeXTheme.COLORS['background'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Center the dialog
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 100, parent.winfo_rooty() + 100))
        
        self.setup_dialog()
    
    def setup_dialog(self):
        """Setup the quick add dialog."""
        main_frame = BeybladeXTheme.create_frame(self.dialog, 'background')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        BeybladeXTheme.create_label(
            main_frame,
            "Quick Add Parts to Collection",
            'heading_medium'
        ).pack(pady=(0, 20))
        
        # Instructions
        BeybladeXTheme.create_label(
            main_frame,
            "Select multiple parts and add them quickly:",
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(pady=(0, 15))
        
        # Part selection area
        selection_frame = BeybladeXTheme.create_card_frame(main_frame)
        selection_frame.pack(fill='both', expand=True, pady=(0, 20))
        
        # Quick selection checkboxes by category
        self.create_quick_selection(selection_frame)
        
        # Bottom buttons
        button_frame = BeybladeXTheme.create_frame(main_frame, 'background')
        button_frame.pack(fill='x')
        
        BeybladeXTheme.create_button(
            button_frame,
            "Add Selected",
            'primary',
            command=self.add_selected_parts
        ).pack(side='right', padx=(10, 0))
        
        BeybladeXTheme.create_button(
            button_frame,
            "Cancel",
            'secondary',
            command=self.dialog.destroy
        ).pack(side='right')
    
    def create_quick_selection(self, parent):
        """Create quick selection interface."""
        content_frame = BeybladeXTheme.create_frame(parent, 'surface')
        content_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        # This would contain checkboxes for popular parts
        # For now, simplified to a text message
        BeybladeXTheme.create_label(
            content_frame,
            "Quick selection interface would go here.\nFor now, use the main Parts Manager.",
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(expand=True)
    
    def add_selected_parts(self):
        """Add selected parts to collection."""
        # Implementation for adding selected parts
        messagebox.showinfo("Info", "Quick add functionality coming soon!")
        self.dialog.destroy()
