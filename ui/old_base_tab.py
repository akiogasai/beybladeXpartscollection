"""Base class for UI tabs."""

import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod


class BaseTab(ABC):
    """Base class for UI tabs with common functionality."""
    
    def __init__(self, parent_notebook, title: str):
        self.frame = ttk.Frame(parent_notebook)
        parent_notebook.add(self.frame, text=title)
        self.setup_ui()
    
    @abstractmethod
    def setup_ui(self):
        """Setup the UI components for this tab."""
        pass
    
    @abstractmethod
    def refresh(self):
        """Refresh the content of this tab."""
        pass
    
    def create_treeview(self, columns: tuple, headings: dict, column_widths: dict) -> ttk.Treeview:
        """Create a standardized treeview with scrollbar."""
        tree = ttk.Treeview(self.frame, columns=columns, show='tree headings')
        
        # Set headings
        tree.heading('#0', text=headings.get('#0', 'Name'))
        for col in columns:
            tree.heading(col, text=headings.get(col, col))
        
        # Set column widths
        tree.column('#0', width=column_widths.get('#0', 150))
        for col in columns:
            tree.column(col, width=column_widths.get(col, 100))
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        return tree, scrollbar
    
    def clear_treeview(self, tree: ttk.Treeview):
        """Clear all items from treeview."""
        for item in tree.get_children():
            tree.delete(item)
