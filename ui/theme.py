"""Modern Beyblade X theme system for consistent styling."""

import tkinter as tk
from tkinter import ttk


class BeybladeXTheme:
    """Modern Beyblade X color scheme and styling."""
    
    # Core Beyblade X colors
    COLORS = {
        # Primary blues (main Beyblade X brand colors)
        'primary': '#1E88E5',          # Bright blue
        'primary_dark': '#1565C0',     # Darker blue
        'primary_light': '#42A5F5',    # Lighter blue
        
        # Accent colors for energy and action
        'accent': '#FF6B35',           # Orange-red for energy
        'accent_light': '#FF8A65',     # Light orange
        'success': '#4CAF50',          # Green for positive actions
        'warning': '#FF9800',          # Orange for warnings
        'danger': '#F44336',           # Red for dangerous actions
        
        # Neutral colors for modern look
        'background': '#FAFAFA',       # Very light gray background
        'surface': '#FFFFFF',          # White surface
        'surface_variant': '#F5F5F5',  # Light gray variant
        'outline': '#E0E0E0',          # Light gray outline
        
        # Text colors
        'text_primary': '#212121',     # Dark gray text
        'text_secondary': '#757575',   # Medium gray text
        'text_on_primary': '#FFFFFF', # White text on blue
        'text_disabled': '#BDBDBD',   # Light gray disabled text
        
        # Dark theme elements
        'dark_surface': '#263238',     # Dark blue-gray
        'dark_primary': '#37474F',     # Darker blue-gray
        'dark_text': '#ECEFF1',        # Light text for dark backgrounds
    }
    
    # Font configurations
    FONTS = {
        'heading_large': ('Segoe UI', 18, 'bold'),
        'heading_medium': ('Segoe UI', 14, 'bold'),
        'heading_small': ('Segoe UI', 12, 'bold'),
        'body': ('Segoe UI', 10),
        'body_small': ('Segoe UI', 9),
        'button': ('Segoe UI', 10, 'bold'),
        'monospace': ('Consolas', 10),
    }
    
    # Component styles
    BUTTON_STYLES = {
        'primary': {
            'bg': COLORS['primary'],
            'fg': COLORS['text_on_primary'],
            'activebackground': COLORS['primary_dark'],
            'activeforeground': COLORS['text_on_primary'],
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 20,
            'pady': 8,
        },
        'secondary': {
            'bg': COLORS['surface'],
            'fg': COLORS['text_primary'],
            'activebackground': COLORS['surface_variant'],
            'activeforeground': COLORS['text_primary'],
            'relief': 'solid',
            'borderwidth': 1,
            'padx': 20,
            'pady': 8,
        },
        'success': {
            'bg': COLORS['success'],
            'fg': COLORS['text_on_primary'],
            'activebackground': '#388E3C',
            'activeforeground': COLORS['text_on_primary'],
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 20,
            'pady': 8,
        },
        'danger': {
            'bg': COLORS['danger'],
            'fg': COLORS['text_on_primary'],
            'activebackground': '#D32F2F',
            'activeforeground': COLORS['text_on_primary'],
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 20,
            'pady': 8,
        },
        'accent': {
            'bg': COLORS['accent'],
            'fg': COLORS['text_on_primary'],
            'activebackground': '#E64A19',
            'activeforeground': COLORS['text_on_primary'],
            'relief': 'flat',
            'borderwidth': 0,
            'padx': 20,
            'pady': 8,
        }
    }
    
    @classmethod
    def configure_ttk_style(cls):
        """Configure ttk styles for modern look."""
        style = ttk.Style()
        
        # Configure Notebook (tabs)
        style.configure('TNotebook', 
                       background=cls.COLORS['background'],
                       borderwidth=0)
        style.configure('TNotebook.Tab',
                       background=cls.COLORS['surface'],
                       foreground=cls.COLORS['text_primary'],
                       padding=[20, 10],
                       focuscolor='none')
        style.map('TNotebook.Tab',
                 background=[('selected', cls.COLORS['primary']),
                           ('active', cls.COLORS['primary_light'])],
                 foreground=[('selected', cls.COLORS['text_on_primary']),
                           ('active', cls.COLORS['text_on_primary'])])
        
        # Configure Treeview
        style.configure('Treeview',
                       background=cls.COLORS['surface'],
                       foreground=cls.COLORS['text_primary'],
                       fieldbackground=cls.COLORS['surface'],
                       borderwidth=1,
                       relief='solid')
        style.configure('Treeview.Heading',
                       background=cls.COLORS['primary'],
                       foreground=cls.COLORS['text_on_primary'],
                       relief='flat',
                       borderwidth=0)
        style.map('Treeview.Heading',
                 background=[('active', cls.COLORS['primary_dark'])])
        
        # Configure Entry
        style.configure('TEntry',
                       fieldbackground=cls.COLORS['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=cls.COLORS['outline'])
        style.map('TEntry',
                 bordercolor=[('focus', cls.COLORS['primary'])])
        
        # Configure Combobox
        style.configure('TCombobox',
                       fieldbackground=cls.COLORS['surface'],
                       borderwidth=1,
                       relief='solid',
                       bordercolor=cls.COLORS['outline'])
        style.map('TCombobox',
                 bordercolor=[('focus', cls.COLORS['primary'])])
    
    @classmethod
    def create_button(cls, parent, text, style='primary', command=None, **kwargs):
        """Create a themed button with consistent styling."""
        button_config = cls.BUTTON_STYLES[style].copy()
        button_config.update(kwargs)
        button_config['font'] = cls.FONTS['button']
        
        return tk.Button(parent, text=text, command=command, **button_config)
    
    @classmethod
    def create_label(cls, parent, text, style='body', **kwargs):
        """Create a themed label with consistent styling."""
        label_config = {
            'bg': cls.COLORS['background'],
            'fg': cls.COLORS['text_primary'],
            'font': cls.FONTS[style]
        }
        label_config.update(kwargs)
        
        return tk.Label(parent, text=text, **label_config)
    
    @classmethod
    def create_frame(cls, parent, style='surface', **kwargs):
        """Create a themed frame with consistent styling."""
        frame_config = {
            'bg': cls.COLORS[style],
            'relief': 'flat',
            'borderwidth': 0
        }
        frame_config.update(kwargs)
        
        return tk.Frame(parent, **frame_config)
    
    @classmethod
    def create_card_frame(cls, parent, **kwargs):
        """Create a card-style frame with shadow effect."""
        frame_config = {
            'bg': cls.COLORS['surface'],
            'relief': 'solid',
            'borderwidth': 1,
            'highlightbackground': cls.COLORS['outline'],
            'highlightthickness': 1
        }
        frame_config.update(kwargs)
        
        return tk.Frame(parent, **frame_config)
