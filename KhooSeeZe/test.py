import tkinter as tk

class ScrollableFrame(tk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.interior = tk.Frame(self.canvas)
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas_window = self.canvas.create_window((0,0), window=self.interior, anchor="nw")

        # keep scroll region updated
        def _on_interior_config(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # update scale range when interior size changes
            height = max(1, self.interior.winfo_height() - self.canvas.winfo_height())
            self._scale.configure(from_=0, to=height)
        self.interior.bind("<Configure>", _on_interior_config)

        def _on_canvas_config(event):
            self.canvas.itemconfig(self.canvas_window, width=event.width)
            height = max(1, self.interior.winfo_height() - self.canvas.winfo_height())
            self._scale.configure(from_=0, to=height)
        self.canvas.bind("<Configure>", _on_canvas_config)

    def attach_scale(self, scale):
        # store reference for updates
        self._scale = scale

    def scroll_to(self, value):
        # value is pixel offset from top; convert to fraction for yview_moveto
        max_scroll = max(1, self.interior.winfo_height() - self.canvas.winfo_height())
        frac = float(value) / max_scroll
        self.canvas.yview_moveto(frac)

# example usage
root = tk.Tk()
root.geometry("500x400")

container = tk.Frame(root)
container.pack(fill="both", expand=True)

scrollable = ScrollableFrame(container)
scrollable.pack(side="left", fill="both", expand=True)

# vertical scale on right side
scale = tk.Scale(container, orient="vertical", showvalue=False, command=lambda v: scrollable.scroll_to(float(v)))
scale.pack(side="right", fill="y")
scrollable.attach_scale(scale)

# populate with many widgets (example long text labels)
for i in range(60):
    tk.Label(scrollable.interior, text=f"Item {i+1}: " + "Long text " * (i % 6 + 1), anchor="w", justify="left").pack(fill="x", padx=5, pady=2)

# sync mousewheel to canvas scroll (optional)
def _on_mousewheel(event):
    # delta on Windows/Linux; on macOS use event.delta directly
    delta = -1 * (event.delta // 120) if event.delta else (1 if event.num == 5 else -1)
    scrollable.canvas.yview_scroll(delta, "units")
    # update scale position
    bbox = scrollable.canvas.bbox("all")
    max_scroll = max(1, scrollable.interior.winfo_height() - scrollable.canvas.winfo_height())
    scroll_pos = scrollable.canvas.yview()[0] * max_scroll
    scale.set(int(scroll_pos))

# Windows and Mac: bind to <MouseWheel>; Linux: <Button-4/5>
root.bind_all("<MouseWheel>", _on_mousewheel)
root.bind_all("<Button-4>", _on_mousewheel)
root.bind_all("<Button-5>", _on_mousewheel)

# keep scale updated periodically (ensures correct range after geometry changes)
def update_scale():
    try:
        height = max(1, scrollable.interior.winfo_height() - scrollable.canvas.winfo_height())
        scale.configure(from_=0, to=height)
        # set scale to current scroll position
        scale.set(int(scrollable.canvas.yview()[0] * height))
    finally:
        root.after(100, update_scale)

root.after(100, update_scale)
root.mainloop()