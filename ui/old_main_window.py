"""Main application window for Beyblade X Collection Manager."""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from services.part_service import PartService
from services.stats_service import StatsService
from ui.tabs.collection_tab import CollectionTab
from ui.tabs.database_tab import DatabaseTab
from ui.tabs.combos_tab import CombosTab
from ui.tabs.stats_tab import StatsTab


class MainWindow:
    """Main application window that coordinates all tabs and services."""
    
    def __init__(self):
        """Initialize the main window and all components."""
        try:
            logging.info("Starting Beyblade X Manager...")
            self.root = tk.Tk()
            self.root.title("🌪️ Beyblade X Collection Manager")
            self.root.geometry("1000x700")
            self.root.configure(bg='#2c3e50')
            
            # Initialize services
            logging.info("Initializing services...")
            self.part_service = PartService()
            self.stats_service = StatsService()
            
            # Load collection
            logging.info("Loading collection...")
            self.part_service.load_collection("collection.json")
            
            logging.info("Setting up UI...")
            self.setup_ui()
            logging.info("UI setup complete!")
            
        except Exception as e:
            logging.error(f"Error in __init__: {e}")
            messagebox.showerror("Initialization Error", f"Failed to start application: {e}")
            raise
    
    def setup_ui(self):
        """Setup the main UI components."""
        # Main title
        title_label = tk.Label(self.root, text="🌪️ BEYBLADE X COLLECTION MANAGER 🌪️", 
                              font=('Arial', 16, 'bold'), bg='#2c3e50', fg='#ecf0f1')
        title_label.pack(pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Create tabs
        self.create_tabs()
        
        # Bottom frame for save button
        bottom_frame = tk.Frame(self.root, bg='#2c3e50')
        bottom_frame.pack(fill='x', padx=10, pady=5)
        
        save_btn = tk.Button(bottom_frame, text="💾 Save Collection", 
                            command=self.save_collection, font=('Arial', 10, 'bold'),
                            bg='#27ae60', fg='white', relief='raised')
        save_btn.pack(side='right', padx=5)
        
        refresh_btn = tk.Button(bottom_frame, text="🔄 Refresh All", 
                               command=self.refresh_all_tabs, font=('Arial', 10, 'bold'),
                               bg='#3498db', fg='white', relief='raised')
        refresh_btn.pack(side='right', padx=5)
    
    def create_tabs(self):
        """Create all tab instances."""
        self.collection_tab = CollectionTab(self.notebook, self.part_service)
        self.database_tab = DatabaseTab(self.notebook, self.part_service)
        self.combos_tab = CombosTab(self.notebook, self.part_service)
        self.stats_tab = StatsTab(self.notebook, self.part_service, self.stats_service)
        
        # Store tabs for easy refresh
        self.tabs = [
            self.collection_tab,
            self.database_tab,
            self.combos_tab,
            self.stats_tab
        ]
    
    def refresh_all_tabs(self):
        """Refresh all tabs to ensure consistency."""
        for tab in self.tabs:
            tab.refresh()
    
    def save_collection(self):
        """Save the collection to file."""
        try:
            self.part_service.save_collection("collection.json")
            messagebox.showinfo("Success", "Collection saved successfully!")
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
