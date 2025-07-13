"""Statistics tab for collection analytics."""

import tkinter as tk
from tkinter import ttk
from ui.base_tab import BaseTab
from services.stats_service import StatsService
from services.part_service import PartService


class StatsTab(BaseTab):
    """Tab for displaying collection statistics."""
    
    def __init__(self, parent_notebook, part_service: PartService, stats_service: StatsService):
        self.part_service = part_service
        self.stats_service = stats_service
        super().__init__(parent_notebook, "📊 Statistics")
    
    def setup_ui(self):
        """Setup the stats tab UI."""
        # Stats content
        self.stats_text = tk.Text(self.frame, wrap=tk.WORD, font=('Arial', 10))
        stats_scrollbar = ttk.Scrollbar(self.frame, orient='vertical', command=self.stats_text.yview)
        self.stats_text.configure(yscrollcommand=stats_scrollbar.set)
        
        self.stats_text.pack(side='left', fill='both', expand=True, padx=(10,0), pady=10)
        stats_scrollbar.pack(side='right', fill='y', pady=10)
        
        self.refresh()
    
    def refresh(self):
        """Refresh the statistics content."""
        self.stats_text.delete(1.0, tk.END)
        
        collection = self.part_service.get_collection()
        stats_content = self.stats_service.generate_stats_text(collection)
        
        self.stats_text.insert(1.0, stats_content)
