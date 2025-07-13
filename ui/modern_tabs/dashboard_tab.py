"""Modern dashboard tab with overview and quick actions."""

import tkinter as tk
from tkinter import ttk
from ui.theme import BeybladeXTheme
from models import Collection, PartType
from services.stats_service import StatsService


class DashboardTab:
    """Modern dashboard tab showing collection overview and quick stats."""
    
    def __init__(self, parent_notebook, collection: Collection, stats_service: StatsService, refresh_callback):
        self.collection = collection
        self.stats_service = stats_service
        self.refresh_callback = refresh_callback
        
        # Create main frame
        self.frame = BeybladeXTheme.create_frame(parent_notebook, 'background')
        parent_notebook.add(self.frame, text="🏠 Dashboard")
        
        self.setup_ui()
        self.refresh()
    
    def setup_ui(self):
        """Setup the dashboard UI."""
        # Main scrollable container
        main_frame = BeybladeXTheme.create_frame(self.frame, 'background')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Welcome section
        self.create_welcome_section(main_frame)
        
        # Stats cards
        self.create_stats_cards(main_frame)
        
        # Recent activity / Quick actions
        self.create_quick_actions(main_frame)
    
    def create_welcome_section(self, parent):
        """Create welcome section with collection overview."""
        welcome_card = BeybladeXTheme.create_card_frame(parent)
        welcome_card.pack(fill='x', pady=(0, 20))
        
        welcome_content = BeybladeXTheme.create_frame(welcome_card, 'surface')
        welcome_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        BeybladeXTheme.create_label(
            welcome_content,
            "Welcome to your Beyblade X Collection!",
            'heading_large'
        ).pack(anchor='w')
        
        # Description
        total_parts = len(self.collection.parts)
        total_quantity = sum(part.owned_quantity for part in self.collection.parts)
        
        if total_parts > 0:
            description = f"You have {total_parts} unique parts with {total_quantity} total items in your collection."
        else:
            description = "Start building your collection by adding parts in the Parts Manager tab."
        
        BeybladeXTheme.create_label(
            welcome_content,
            description,
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack(anchor='w', pady=(5, 0))
    
    def create_stats_cards(self, parent):
        """Create stats cards showing collection metrics."""
        stats_frame = BeybladeXTheme.create_frame(parent, 'background')
        stats_frame.pack(fill='x', pady=(0, 20))
        
        # Stats cards container
        cards_container = BeybladeXTheme.create_frame(stats_frame, 'background')
        cards_container.pack(fill='x')
        
        # Calculate stats
        blades = self.collection.get_parts_by_type(PartType.BLADE)
        ratchets = self.collection.get_parts_by_type(PartType.RATCHET)
        bits = self.collection.get_parts_by_type(PartType.BIT)
        combos = len(self.collection.combos)
        
        # Create individual stat cards
        self.create_stat_card(cards_container, "🗡️", "Blades", len(blades), 0)
        self.create_stat_card(cards_container, "⚙️", "Ratchets", len(ratchets), 1)
        self.create_stat_card(cards_container, "🎯", "Bits", len(bits), 2)
        self.create_stat_card(cards_container, "⚔️", "Combos", combos, 3)
    
    def create_stat_card(self, parent, icon, label, value, position):
        """Create an individual stat card."""
        card = BeybladeXTheme.create_card_frame(parent)
        card.grid(row=0, column=position, padx=10, pady=0, sticky='ew')
        
        # Configure grid weights for equal distribution
        parent.grid_columnconfigure(position, weight=1)
        
        # Card content
        content = BeybladeXTheme.create_frame(card, 'surface')
        content.pack(fill='both', expand=True, padx=15, pady=15)
        
        # Icon
        BeybladeXTheme.create_label(
            content,
            icon,
            'heading_large'
        ).pack()
        
        # Value
        BeybladeXTheme.create_label(
            content,
            str(value),
            'heading_large',
            fg=BeybladeXTheme.COLORS['primary']
        ).pack()
        
        # Label
        BeybladeXTheme.create_label(
            content,
            label,
            'body',
            fg=BeybladeXTheme.COLORS['text_secondary']
        ).pack()
    
    def create_quick_actions(self, parent):
        """Create quick actions section."""
        actions_card = BeybladeXTheme.create_card_frame(parent)
        actions_card.pack(fill='x')
        
        actions_content = BeybladeXTheme.create_frame(actions_card, 'surface')
        actions_content.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Title
        BeybladeXTheme.create_label(
            actions_content,
            "Quick Actions",
            'heading_medium'
        ).pack(anchor='w', pady=(0, 15))
        
        # Buttons container
        buttons_frame = BeybladeXTheme.create_frame(actions_content, 'surface')
        buttons_frame.pack(fill='x')
        
        # Quick action buttons
        BeybladeXTheme.create_button(
            buttons_frame,
            "🎯 Browse All Parts",
            'primary',
            command=self.go_to_parts_manager
        ).pack(side='left', padx=(0, 10))
        
        BeybladeXTheme.create_button(
            buttons_frame,
            "⚔️ Create New Combo",
            'accent',
            command=self.go_to_combos
        ).pack(side='left', padx=(0, 10))
        
        if len(self.collection.parts) > 0:
            BeybladeXTheme.create_button(
                buttons_frame,
                "📊 View Detailed Stats",
                'secondary',
                command=self.show_detailed_stats
            ).pack(side='left')
    
    def go_to_parts_manager(self):
        """Switch to All Parts tab."""
        # Get parent notebook and switch to All Parts tab (index 1)
        notebook = self.frame.master
        notebook.select(1)
    
    def go_to_combos(self):
        """Switch to combos tab."""
        # Get parent notebook and switch to combos tab (index 3)
        notebook = self.frame.master
        notebook.select(3)
    
    def show_detailed_stats(self):
        """Show detailed statistics in a popup."""
        from tkinter import messagebox
        stats_text = self.stats_service.calculate_stats(self.collection)
        messagebox.showinfo("Detailed Statistics", stats_text)
    
    def refresh(self):
        """Refresh the dashboard content."""
        # Refresh is handled by recreating the stats cards
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.setup_ui()
