"""
main GUI window
"""
from constants import *
from tk_formatter import TkFormatter


class StockManagement:
    """
    class to start, manage stock management GUI
    """

    def __init__(self):
        """
        initialising instance of tkinter on main window
        """
        tk_format = TkFormatter(GUI_TOP_TITLE, GUI_GEOMETRY, GUI_BG_COLOR)
        tk_format.crate_tk_window()


# starting software
StockManagement()
