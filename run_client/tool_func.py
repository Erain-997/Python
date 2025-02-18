# _*_coding:utf-8_*_
# Author：zyr
# Time：2024/11/15
import tkinter as tk


class ToolFunc:
    def __init__(self, widget, text, delay=300):  # 默认延时1秒
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tip_window = None
        self.id = None
        self.widget.bind("<Enter>", self.schedule_show_tip)
        self.widget.bind("<Leave>", self.hide_tip)

    def schedule_show_tip(self, event=None):
        if self.id:
            self.widget.after_cancel(self.id)
        self.id = self.widget.after(self.delay, self.show_tip)

    def show_tip(self, event=None):
        x, y, _, _ = self.widget.bbox("insert")
        x += self.widget.winfo_rootx() + 25
        y += self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=self.text, background="#ffffe0", relief="solid", borderwidth=1
        )
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None
        if self.id:
            self.widget.after_cancel(self.id)
            self.id = None


