#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 4.21
#  in conjunction with Tcl version 8.6
#    May 10, 2019 05:46:41 PM +0800  platform: Windows NT

print('Starting GUI...')

import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk

    py3 = False
except ImportError:
    import tkinter.ttk as ttk

    py3 = True

import ReliabilityDriftProgram_support
import os.path


def vp_start_gui():
    """Starting point when module is the main routine."""
    global w, root
    global prog_location
    prog_call = sys.argv[0]
    print("prog_call = {}".format(prog_call))
    prog_location = os.path.split(prog_call)[0]
    print("prog_location = {}".format(prog_location))
    sys.stdout.flush()
    root = tk.Tk()
    top = Toplevel1(root)
    ReliabilityDriftProgram_support.init(root, top)
    root.mainloop()


w = None


def create_Toplevel1(root, *args, **kwargs):
    """Starting point when module is imported by another program."""
    global w, rt
    global prog_location
    prog_call = sys.argv[0]
    print("prog_call = {}".format(prog_call))
    prog_location = os.path.split(prog_call)[0]
    print("prog_location = {}".format(prog_location))
    rt = root
    w = tk.Toplevel(root)
    top = Toplevel1(w)
    ReliabilityDriftProgram_support.init(w, top, *args, **kwargs)
    return (w, top)


def destroy_Toplevel1():
    global w
    w.destroy()
    w = None


class Toplevel1:
    def __init__(self, top=None):
        """This class configures and populates the toplevel window.
           top is the toplevel containing window."""
        _bgcolor = "#d9d9d9"  # X11 color: 'gray85'
        _fgcolor = "#000000"  # X11 color: 'black'
        _compcolor = "#d9d9d9"  # X11 color: 'gray85'
        _ana1color = "#d9d9d9"  # X11 color: 'gray85'
        _ana2color = "#ececec"  # Closest X11 color: 'gray92'

        top.geometry("600x575+650+250")
        top.title("AMS Tampines Reliability Drift Analysis Platform")
        top.configure(background="#ffffff")
        top.configure(highlightbackground="#ffffff")
        top.configure(highlightcolor="black")
        top.configure(takefocus="1")

        self.Label3 = tk.Label(top)
        self.Label3.place(relx=0.033, rely=0.174, height=56, width=552)
        self.Label3.configure(background="#ffffff")
        self.Label3.configure(font="-family {Segoe UI} -size 14 -weight bold")
        self.Label3.configure(foreground="#3d3d3d")
        self.Label3.configure(
            text="""AMS TAMPINES RELIABILITY DRIFT ANALYSIS PLATFORM"""
        )
        self.Label3.configure(wraplength="400")

        self.database_frame = tk.LabelFrame(top)
        self.database_frame.place(
            relx=0.117, rely=0.296, relheight=0.165, relwidth=0.75
        )
        self.database_frame.configure(relief="groove")
        self.database_frame.configure(font="-family {Segoe UI} -size 9")
        self.database_frame.configure(foreground="#1e1e1e")
        self.database_frame.configure(labelanchor="n")
        self.database_frame.configure(text="""Database Options""")
        self.database_frame.configure(background="#ffffff")
        self.database_frame.configure(highlightcolor="black")
        self.database_frame.configure(width=400)

        self.drift_calculation_button = tk.Button(self.database_frame)
        self.drift_calculation_button.place(
            relx=0.511, rely=0.316, height=53, width=196, bordermode="ignore"
        )
        self.drift_calculation_button.configure(activebackground="#79bcff")
        self.drift_calculation_button.configure(background="#ececec")
        self.drift_calculation_button.configure(
            command=ReliabilityDriftProgram_support.drift_calculation
        )
        self.drift_calculation_button.configure(pady="0")
        self.drift_calculation_button.configure(relief="flat")
        self.drift_calculation_button.configure(
            text="""2. Compute Drift from Database (Select Files)"""
        )
        self.drift_calculation_button.configure(wraplength="180")
        tooltip_font = "TkDefaultFont"
        ToolTip(
            self.drift_calculation_button,
            tooltip_font,
            """Select the folder for which you would like to\ncalculate drift metrics for.\n\n选择要为其计算DRIFT的RTO文件夹。""",
            delay=0.2,
        )

        self.build_database_button = tk.Button(self.database_frame)
        self.build_database_button.place(
            relx=0.044, rely=0.316, height=53, width=196, bordermode="ignore"
        )
        self.build_database_button.configure(activebackground="#79bcff")
        self.build_database_button.configure(background="#ececec")
        self.build_database_button.configure(
            command=ReliabilityDriftProgram_support.build_database
        )
        self.build_database_button.configure(highlightcolor="black")
        self.build_database_button.configure(pady="0")
        self.build_database_button.configure(relief="flat")
        self.build_database_button.configure(
            text="1. Compile Files to Database (Select Folder)"
        )
        self.build_database_button.configure(wraplength="180")
        tooltip_font = "TkDefaultFont"
        ToolTip(
            self.build_database_button,
            tooltip_font,
            """Click to select files belonging to a single RTO\nto add them to a database for that RTO.\n\n通过选择RTO文件夹将文件编译到数据库.""",
            delay=0.2,
        )

        self.plotting_frame = tk.LabelFrame(top)
        self.plotting_frame.place(
            relx=0.117, rely=0.487, relheight=0.165, relwidth=0.75
        )
        self.plotting_frame.configure(relief="groove")
        self.plotting_frame.configure(font="-family {Segoe UI} -size 9")
        self.plotting_frame.configure(foreground="#1e1e1e")
        self.plotting_frame.configure(labelanchor="n")
        self.plotting_frame.configure(text="""Raw Data Plotting Options""")
        self.plotting_frame.configure(background="#ffffff")
        self.plotting_frame.configure(highlightbackground="#d9d9d9")
        self.plotting_frame.configure(highlightcolor="black")
        self.plotting_frame.configure(width=400)

        self.folder_save_img_button = tk.Button(self.plotting_frame)
        self.folder_save_img_button.place(
            relx=0.511, rely=0.316, height=53, width=196, bordermode="ignore"
        )
        self.folder_save_img_button.configure(activebackground="#79bcff")
        self.folder_save_img_button.configure(background="#ececec")
        self.folder_save_img_button.configure(
            command=ReliabilityDriftProgram_support.folder_save_img
        )
        self.folder_save_img_button.configure(pady="0")
        self.folder_save_img_button.configure(relief="flat")
        self.folder_save_img_button.configure(
            text="""3b. Plot Database Files in Folder (Save to .jpg)"""
        )
        self.folder_save_img_button.configure(wraplength="180")
        tooltip_font = "TkDefaultFont"
        ToolTip(
            self.folder_save_img_button,
            tooltip_font,
            """Select a folder containing the database files\ncreated with '1. Compile Files to Database' that you\nwould like to plot.\n\n选择包含要使用'1. Compile Files to Database'\n创建的数据库文件的文件夹。""",
            delay=0.2,
        )

        self.file_plot_interactive_button = tk.Button(self.plotting_frame)
        self.file_plot_interactive_button.place(
            relx=0.044, rely=0.316, height=53, width=196, bordermode="ignore"
        )
        self.file_plot_interactive_button.configure(activebackground="#79bcff")
        self.file_plot_interactive_button.configure(background="#ececec")
        self.file_plot_interactive_button.configure(
            command=ReliabilityDriftProgram_support.file_plot_interactive
        )
        self.file_plot_interactive_button.configure(pady="0")
        self.file_plot_interactive_button.configure(relief="flat")
        self.file_plot_interactive_button.configure(
            text="""3a. Select Database File to Plot (Interactive)"""
        )
        self.file_plot_interactive_button.configure(wraplength="180")
        tooltip_font = "TkDefaultFont"
        ToolTip(
            self.file_plot_interactive_button,
            tooltip_font,
            """Select files to view an interactive plot without\nsaving them to a database.\n\n选择文件以查看交互式绘图而不将其保存到数据库。""",
            delay=0.2,
        )

        self.plotting_frame_4 = tk.LabelFrame(top)
        self.plotting_frame_4.place(
            relx=0.117, rely=0.678, relheight=0.165, relwidth=0.75
        )
        self.plotting_frame_4.configure(relief="groove")
        self.plotting_frame_4.configure(font="-family {Segoe UI} -size 9")
        self.plotting_frame_4.configure(foreground="#1e1e1e")
        self.plotting_frame_4.configure(labelanchor="n")
        self.plotting_frame_4.configure(text="""Drift Plotting Options""")
        self.plotting_frame_4.configure(background="#ffffff")
        self.plotting_frame_4.configure(highlightbackground="#d9d9d9")
        self.plotting_frame_4.configure(highlightcolor="black")
        self.plotting_frame_4.configure(width=400)

        self.folder_drift_save_img_button = tk.Button(self.plotting_frame_4)
        self.folder_drift_save_img_button.place(
            relx=0.511, rely=0.316, height=53, width=196, bordermode="ignore"
        )
        self.folder_drift_save_img_button.configure(activebackground="#79bcff")
        self.folder_drift_save_img_button.configure(background="#ececec")
        self.folder_drift_save_img_button.configure(
            command=ReliabilityDriftProgram_support.folder_drift_save_img
        )
        self.folder_drift_save_img_button.configure(pady="0")
        self.folder_drift_save_img_button.configure(relief="flat")
        self.folder_drift_save_img_button.configure(
            text="""4b. Plot All Drift In Folder (Save to .jpg)"""
        )
        self.folder_drift_save_img_button.configure(wraplength="150")
        tooltip_font = "TkDefaultFont"
        ToolTip(
            self.folder_drift_save_img_button,
            tooltip_font,
            """Select a folder containing the files you would\nlike to plot calculated drift for.\n\n选择一个RTO文件夹，其中包含您要为其计算\nDRIFT的文件。""",
            delay=0.2,
        )

        self.drift_plot_interactive_button = tk.Button(self.plotting_frame_4)
        self.drift_plot_interactive_button.place(
            relx=0.044, rely=0.316, height=53, width=196, bordermode="ignore"
        )
        self.drift_plot_interactive_button.configure(activebackground="#79bcff")
        self.drift_plot_interactive_button.configure(background="#ececec")
        self.drift_plot_interactive_button.configure(
            command=ReliabilityDriftProgram_support.drift_plot_interactive
        )
        self.drift_plot_interactive_button.configure(pady="0")
        self.drift_plot_interactive_button.configure(relief="flat")
        self.drift_plot_interactive_button.configure(
            text="""4a. Select Drift To Plot (Interactive)"""
        )
        self.drift_plot_interactive_button.configure(wraplength="150")
        tooltip_font = "TkDefaultFont"
        ToolTip(
            self.drift_plot_interactive_button,
            tooltip_font,
            """Select drift files to view an interactive plot\nwithout saving them to a database.\n\n选择DRIFT文件以查看交互式绘图而不将其\n保存到数据库。""",
            delay=0.2,
        )
        
        try:
            self.Label1 = tk.Label(top)
            self.Label1.place(relx=0.333, rely=0.061, height=53, width=176)
            self.Label1.configure(background="#ffffff")

            photo_location = os.path.join(prog_location, "amslogo.png")
            self._img0 = tk.PhotoImage(file=photo_location)

            self.Label1.configure(image=self._img0)
            self.Label1.configure(text="""Label""")
            tooltip_font = "TkDefaultFont"
            ToolTip(
                self.Label1,
                tooltip_font,
                """Created by Tampines Quality Department\nEvan Chong, 2019\nQuality Intern""",
                delay=0.2,
            )
        except:
            pass

        self.menubar = tk.Menu(top, font="TkMenuFont", bg=_bgcolor, fg=_fgcolor)
        top.configure(menu=self.menubar)

        self.DoAll = tk.Button(top)
        self.DoAll.place(relx=0.0, rely=0.939, height=33, width=125)
        self.DoAll.configure(activebackground="#ffffff")
        self.DoAll.configure(activeforeground="#ffffff")
        self.DoAll.configure(background="#ffffff")
        self.DoAll.configure(command=ReliabilityDriftProgram_support.DoAll)
        self.DoAll.configure(disabledforeground="#a3a3a3")
        self.DoAll.configure(foreground="#adadad")
        self.DoAll.configure(highlightbackground="#d9d9d9")
        self.DoAll.configure(highlightcolor="#ffffff")
        self.DoAll.configure(pady="0")
        self.DoAll.configure(relief="flat")
        self.DoAll.configure(text="""Execute Order 66""")
        ToolTip(
            self.DoAll,
            tooltip_font,
            """Generate Database, Raw Data Plots, Drift Calculation, Drift Plots for a selected RTO folder.""",
            delay=0.2,
        )


# ======================================================
# Modified by Rozen to remove Tkinter import statements and to receive
# the font as an argument.
# ======================================================
# Found the original code at:
# http://code.activestate.com/recipes/576688-tooltip-for-tkinter/
# ======================================================
# How to use this class...
#   Copy the file tooltip.py into your working directory
#   import this into the _support python file created by Page
#   from tooltip import ToolTip
#   in the _support python file, create a function to attach each tooltip
#   to the widgets desired. Example:
#   ToolTip(self.widgetname, font, msg='Exit program', follow=False, delay=0.2)
# ======================================================
from time import time, localtime, strftime


class ToolTip(tk.Toplevel):
    """
    Provides a ToolTip widget for Tkinter.
    To apply a ToolTip to any Tkinter widget, simply pass the widget to the
    ToolTip constructor
    """

    def __init__(
        self, wdgt, tooltip_font, msg=None, msgFunc=None, delay=1, follow=True
    ):
        """
        Initialize the ToolTip

        Arguments:
          wdgt: The widget this ToolTip is assigned to
          tooltip_font: Font to be used
          msg:  A static string message assigned to the ToolTip
          msgFunc: A function that retrieves a string to use as the ToolTip text
          delay:   The delay in seconds before the ToolTip appears(may be float)
          follow:  If True, the ToolTip follows motion, otherwise hides
        """
        self.wdgt = wdgt
        # The parent of the ToolTip is the parent of the ToolTips widget
        self.parent = self.wdgt.master
        # Initalise the Toplevel
        tk.Toplevel.__init__(self, self.parent, bg="black", padx=1, pady=1)
        # Hide initially
        self.withdraw()
        # The ToolTip Toplevel should have no frame or title bar
        self.overrideredirect(True)

        # The msgVar will contain the text displayed by the ToolTip
        self.msgVar = tk.StringVar()
        if msg is None:
            self.msgVar.set("No message provided")
        else:
            self.msgVar.set(msg)
        self.msgFunc = msgFunc
        self.delay = delay
        self.follow = follow
        self.visible = 0
        self.lastMotion = 0
        # The text of the ToolTip is displayed in a Message widget
        tk.Message(
            self, textvariable=self.msgVar, bg="#e3f1ff", font=tooltip_font, aspect=1000
        ).grid()

        # Add bindings to the widget.  This will NOT override
        # bindings that the widget already has
        self.wdgt.bind("<Enter>", self.spawn, "+")
        self.wdgt.bind("<Leave>", self.hide, "+")
        self.wdgt.bind("<Motion>", self.move, "+")

    def spawn(self, event=None):
        """
        Spawn the ToolTip.  This simply makes the ToolTip eligible for display.
        Usually this is caused by entering the widget

        Arguments:
          event: The event that called this funciton
        """
        self.visible = 1
        # The after function takes a time argument in miliseconds
        self.after(int(self.delay * 1000), self.show)

    def show(self):
        """
        Displays the ToolTip if the time delay has been long enough
        """
        if self.visible == 1 and time() - self.lastMotion > self.delay:
            self.visible = 2
        if self.visible == 2:
            self.deiconify()

    def move(self, event):
        """
        Processes motion within the widget.
        Arguments:
          event: The event that called this function
        """
        self.lastMotion = time()
        # If the follow flag is not set, motion within the
        # widget will make the ToolTip disappear
        #
        if self.follow is False:
            self.withdraw()
            self.visible = 1

        # Offset the ToolTip 10x10 pixes southwest of the pointer
        self.geometry("+%i+%i" % (event.x_root + 20, event.y_root - 10))
        try:
            # Try to call the message function.  Will not change
            # the message if the message function is None or
            # the message function fails
            self.msgVar.set(self.msgFunc())
        except:
            pass
        self.after(int(self.delay * 1000), self.show)

    def hide(self, event=None):
        """
        Hides the ToolTip.  Usually this is caused by leaving the widget
        Arguments:
          event: The event that called this function
        """
        self.visible = 0
        self.withdraw()


# ===========================================================
#                   End of Class ToolTip
# ===========================================================

if __name__ == "__main__":
    vp_start_gui()

