"""Modern main window with improved Beyblade X design."""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from services.part_service import PartService
from services.stats_service import StatsService
from ui.theme import BeybladeXTheme
from ui.modern_tabs.dashboard_tab import DashboardTab
from ui.modern_tabs.parts_tab import PartsTab
from ui.modern_tabs.parts_manager_tab import PartsManagerTab
from ui.modern_tabs.combos_tab import CombosTab
from data.persistence import save_collection, load_collection


class ModernMainWindow:
    """Modern, redesigned main window with Beyblade X theming."""
    
    def __init__(self):
        """Initialize the modern main window."""
        try:
            logging.info("Starting Modern Beyblade X Manager...")
            self.root = tk.Tk()
            self.root.title("Beyblade X Collection Manager")
            self.root.geometry("1200x800")
            self.root.configure(bg=BeybladeXTheme.COLORS['background'])
            
            # Set minimum size
            self.root.minsize(1000, 600)
            
            # Initialize services
            logging.info("Initializing services...")
            self.collection = load_collection()
            self.part_service = PartService()
            self.stats_service = StatsService()
            
            # Configure theme
            BeybladeXTheme.configure_ttk_style()
            
            logging.info("Setting up modern UI...")
            self.setup_ui()
            logging.info("UI setup complete!")
            
        except Exception as e:
            logging.error(f"Error in __init__: {e}")
            messagebox.showerror("Initialization Error", f"Failed to start application: {e}")
            raise
    
    def setup_ui(self):
        """Setup the modern UI with better layout."""
        # Header section
        self.create_header()
        
        # Main content area
        self.create_main_content()
        
        # Status bar
        self.create_status_bar()
    
    def create_header(self):
        """Create modern header with title and quick actions."""
        header_frame = BeybladeXTheme.create_frame(self.root, 'primary')
        header_frame.pack(fill='x', padx=0, pady=0)
        
        # Title section
        title_frame = BeybladeXTheme.create_frame(header_frame, 'primary')
        title_frame.pack(side='left', fill='both', expand=True, padx=20, pady=15)
        
        # Main title
        title_label = BeybladeXTheme.create_label(
            title_frame, 
            "⚡ BEYBLADE X", 
            'heading_large',
            bg=BeybladeXTheme.COLORS['primary'],
            fg=BeybladeXTheme.COLORS['text_on_primary']
        )
        title_label.pack(side='left')
        
        # Subtitle
        subtitle_label = BeybladeXTheme.create_label(
            title_frame,
            "Collection Manager",
            'heading_medium',
            bg=BeybladeXTheme.COLORS['primary'],
            fg=BeybladeXTheme.COLORS['text_on_primary']
        )
        subtitle_label.pack(side='left', padx=(10, 0))
        
        # Quick actions frame
        actions_frame = BeybladeXTheme.create_frame(header_frame, 'primary')
        actions_frame.pack(side='right', padx=20, pady=15)
        
        # Quick action buttons
        BeybladeXTheme.create_button(
            actions_frame, "💾 Save", 'secondary',
            command=self.save_collection
        ).pack(side='right', padx=5)
        
        BeybladeXTheme.create_button(
            actions_frame, "🔄 Refresh", 'secondary',
            command=self.refresh_all
        ).pack(side='right', padx=5)
    
    def create_main_content(self):
        """Create the main content area with modern tabs."""
        # Main container
        main_container = BeybladeXTheme.create_frame(self.root, 'background')
        main_container.pack(fill='both', expand=True, padx=20, pady=(10, 20))
        
        # Create modern notebook
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill='both', expand=True)
        
        # Create modern tabs
        self.create_modern_tabs()
    
    def create_modern_tabs(self):
        """Create modernized tabs with better UX."""
        # Dashboard - Overview and quick stats
        self.dashboard_tab = DashboardTab(
            self.notebook, 
            self.collection, 
            self.stats_service,
            self.refresh_callback
        )
        
        # All Parts - Comprehensive parts browser
        self.all_parts_tab = PartsTab(
            self.notebook,
            self.collection,
            self.refresh_callback
        )
        
        # Parts Manager - Combined collection and database view
        self.parts_manager_tab = PartsManagerTab(
            self.notebook,
            self.collection,
            self.part_service,
            self.refresh_callback
        )
        
        # Combos - Streamlined combo management
        self.combos_tab = CombosTab(
            self.notebook,
            self.collection,
            self.refresh_callback
        )
        
        # Store tabs for easy refresh
        self.tabs = [
            self.dashboard_tab,
            self.all_parts_tab,
            self.parts_manager_tab,
            self.combos_tab
        ]
    
    def create_status_bar(self):
        """Create status bar with collection info."""
        status_frame = BeybladeXTheme.create_frame(self.root, 'surface_variant')
        status_frame.pack(fill='x', side='bottom')
        
        # Collection stats
        self.status_label = BeybladeXTheme.create_label(
            status_frame,
            self.get_status_text(),
            'body_small',
            bg=BeybladeXTheme.COLORS['surface_variant'],
            fg=BeybladeXTheme.COLORS['text_secondary']
        )
        self.status_label.pack(side='left', padx=10, pady=5)
        
        # App info
        app_info = BeybladeXTheme.create_label(
            status_frame,
            "Ready",
            'body_small',
            bg=BeybladeXTheme.COLORS['surface_variant'],
            fg=BeybladeXTheme.COLORS['text_secondary']
        )
        app_info.pack(side='right', padx=10, pady=5)
    
    def get_status_text(self):
        """Get current collection status text."""
        total_parts = len(self.collection.parts)
        total_quantity = sum(part.owned_quantity for part in self.collection.parts)
        total_combos = len(self.collection.combos)
        
        return f"Collection: {total_parts} unique parts • {total_quantity} total items • {total_combos} combos"
    
    def refresh_callback(self):
        """Callback function for tabs to trigger full refresh."""
        self.refresh_all()
    
    def refresh_all(self):
        """Refresh all tabs and status."""
        for tab in self.tabs:
            if hasattr(tab, 'refresh'):
                tab.refresh()
        
        # Update status bar
        self.status_label.config(text=self.get_status_text())
    
    def save_collection(self):
        """Save the collection to file."""
        try:
            save_collection(self.collection, "collection.json")
            messagebox.showinfo("Success", "Collection saved successfully!")
            self.status_label.config(text=self.get_status_text() + " • Saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save collection: {e}")
    
    def run(self):
        """Start the application main loop."""
        try:
            logging.info("Entering main loop...")
            self.root.mainloop()
        except Exception as e:
            logging.error(f"Error in main loop: {e}")
            messagebox.showerror("Runtime Error", f"Application error: {e}")
