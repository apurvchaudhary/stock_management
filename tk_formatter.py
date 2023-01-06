"""
tkinter formatter utility
"""
import tkinter as tk
from constants import *


class TkFormatter:
    """
    class to interact with tkinter
    """

    def __init__(self, title, geometry, gui_bg_color):
        self.title = title
        self.geometry = geometry
        self.gui_bg_color = gui_bg_color

    def crate_tk_window(self):
        """
        tkinter window creation
        :return: tkinter window
        """
        window = tk.Tk()
        window.title(self.title)
        width = window.winfo_screenwidth()
        height = window.winfo_screenheight()
        window.geometry("%dx%d" % (width, height))
        window.configure(background=self.gui_bg_color)
        self.create_tk_label(text=GUI_IN_TITLE, bg_color=GUI_IN_TITLE_BG_COLOR, font=GUI_IN_TITLE_FONT,
                             height=GUI_IN_TITLE_HEIGHT, width=int(window.winfo_screenwidth()/10))
        window.mainloop()
        return window

    @staticmethod
    def create_tk_label(
        text,
        fg_color=None,
        bg_color=None,
        font=None,
        height=None,
        width=None,
        row=None,
        sticky=None,
        padx=None,
        pady=None,
    ):
        """
        method to create tkinter label with given params
        :param pady: padding y
        :param padx: padding x
        :param sticky:
        :param row:
        :param fg_color: "red
        :param text: "test"
        :param bg_color: "red"
        :param font: ("Times", "22", "bold")
        :param height: 1
        :param width: 10
        :return: tkinter label
        """
        prompt = tk.Label(text=text, font=font, fg=fg_color, bg=bg_color, height=height, width=width)
        prompt.grid(row=row, sticky=sticky, pady=pady, padx=padx)

    @staticmethod
    def create_tk_entry_field(width, row, padx, pady, sticky):
        """
        method to create tkinter entry field
        :param width:
        :param row:
        :param padx:
        :param pady:
        :param sticky:
        :return:
        """
        entry_field = tk.Entry(width=width)
        entry_field.grid(row=row, sticky=sticky, padx=padx, pady=pady)
