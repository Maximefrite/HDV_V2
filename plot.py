#!/usr/bin/env python3
# plot_gui.py
# Local desktop GUI to explore expanded_prices_output.csv
# No web server, no internet.

import os
import re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import pandas as pd
import matplotlib
matplotlib.use("TkAgg")  # Tkinter backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


CSV_FILE = "expanded_prices_output.csv"


def load_long_df(csv_path: str) -> pd.DataFrame:
    """
    Load the wide CSV and convert to a long tidy dataframe:
    columns: Resource | YYYYMMDD_HHMMSS (one or more)
    Output columns: BaseResource | Unit | Date | Price
    """
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    if "Resource" not in df.columns:
        raise ValueError("CSV must contain a 'Resource' column.")

    # Melt wide -> long
    melted = df.melt(id_vars="Resource", var_name="Date", value_name="Price")

    # Extract unit from Resource like "Iron (10 unit)"
    melted["Unit"] = melted["Resource"].str.extract(r"\((\d+)\s*unit\)", expand=False)
    # Base name without "(x unit)"
    melted["BaseResource"] = melted["Resource"].str.replace(r"\s*\(\d+\s*unit\)\s*$", "", regex=True)

    # Parse dates from column names (e.g., 20251027_142455). Coerce invalid to NaT.
    # If your headers are like that, this will work; otherwise adjust the format/try parse.
    def parse_dt(x: str):
        # Accept bare strings that look like YYYYMMDD_HHMMSS; otherwise try pandas to_datetime
        if isinstance(x, str) and re.fullmatch(r"\d{8}_\d{6}", x):
            try:
                return pd.to_datetime(x, format="%Y%m%d_%H%M%S")
            except Exception:
                return pd.NaT
        try:
            return pd.to_datetime(x)
        except Exception:
            return pd.NaT

    melted["Date"] = melted["Date"].map(parse_dt)
    # Clean numeric
    def to_num(v):
        if pd.isna(v):
            return pd.NA
        if isinstance(v, str):
            digits = re.sub(r"[^\d]", "", v)
            if digits == "":
                return pd.NA
            try:
                return int(digits)
            except Exception:
                return pd.NA
        return v

    melted["Price"] = melted["Price"].map(to_num)

    # Keep valid rows only
    melted = melted.dropna(subset=["Date", "Unit", "BaseResource"])
    melted = melted.sort_values(["BaseResource", "Unit", "Date"])
    return melted


class PriceGUI(tk.Tk):
    def __init__(self, csv_path=CSV_FILE):
        super().__init__()
        self.title("Resource Price Viewer")
        self.geometry("1000x700")
        self.minsize(800, 600)

        self.csv_path = csv_path
        try:
            self.long_df = load_long_df(self.csv_path)
        except Exception as e:
            messagebox.showerror("Error loading CSV", str(e))
            self.long_df = pd.DataFrame(columns=["BaseResource", "Unit", "Date", "Price"])

        # UI: controls frame
        ctrl = ttk.Frame(self, padding=10)
        ctrl.pack(side=tk.TOP, fill=tk.X)

        # Resource dropdown
        ttk.Label(ctrl, text="Resource:").pack(side=tk.LEFT, padx=(0, 6))
        self.resource_var = tk.StringVar()
        self.resource_cb = ttk.Combobox(ctrl, textvariable=self.resource_var, state="readonly", width=40)
        self.resource_cb.pack(side=tk.LEFT, padx=(0, 12))

        # Unit radios
        ttk.Label(ctrl, text="Unit:").pack(side=tk.LEFT, padx=(0, 6))
        self.unit_var = tk.StringVar(value="1")
        for u in ["1", "10", "100"]:
            ttk.Radiobutton(ctrl, text=u, value=u, variable=self.unit_var, command=self.update_plot)\
                .pack(side=tk.LEFT)

        # Spacer
        ttk.Label(ctrl, text="   ").pack(side=tk.LEFT)

        # Buttons
        ttk.Button(ctrl, text="Refresh CSV", command=self.refresh_csv).pack(side=tk.LEFT, padx=6)
        ttk.Button(ctrl, text="Open CSV�", command=self.choose_csv).pack(side=tk.LEFT, padx=6)
        ttk.Button(ctrl, text="Save Chart as PNG�", command=self.save_png).pack(side=tk.LEFT, padx=6)

        # Figure + canvas
        self.fig = Figure(figsize=(8, 5), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Matplotlib toolbar
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()

        # Status bar
        self.status = tk.StringVar(value="")
        statusbar = ttk.Label(self, textvariable=self.status, anchor="w")
        statusbar.pack(side=tk.BOTTOM, fill=tk.X)

        self.populate_resources()
        self.bind_events()
        self.update_plot(initial=True)

    def bind_events(self):
        self.resource_cb.bind("<<ComboboxSelected>>", lambda e: self.update_plot())

    def populate_resources(self):
        resources = sorted(self.long_df["BaseResource"].unique())
        self.resource_cb["values"] = resources
        if resources:
            # Keep selection if still present, else choose first
            current = self.resource_var.get()
            if current in resources:
                self.resource_cb.set(current)
            else:
                self.resource_cb.current(0)

    def refresh_csv(self):
        try:
            self.long_df = load_long_df(self.csv_path)
            self.populate_resources()
            self.update_plot()
            self.status.set(f"Reloaded {self.csv_path}")
        except Exception as e:
            messagebox.showerror("Error reloading CSV", str(e))

    def choose_csv(self):
        path = filedialog.askopenfilename(
            title="Select CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if path:
            self.csv_path = path
            self.refresh_csv()

    def save_png(self):
        path = filedialog.asksaveasfilename(
            title="Save Chart As",
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")]
        )
        if path:
            try:
                self.fig.savefig(path, bbox_inches="tight")
                self.status.set(f"Saved: {path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def update_plot(self, initial=False):
        if self.long_df.empty:
            self.ax.clear()
            self.ax.set_title("No data")
            self.canvas.draw_idle()
            return

        resource = self.resource_var.get() or (self.resource_cb["values"][0] if self.resource_cb["values"] else "")
        unit = self.unit_var.get()

        dff = self.long_df[(self.long_df["BaseResource"] == resource) & (self.long_df["Unit"] == unit)].copy()

        self.ax.clear()

        if dff.empty:
            self.ax.set_title(f"No data for: {resource} (unit {unit})")
            self.ax.set_xlabel("Time")
            self.ax.set_ylabel("Price")
            self.canvas.draw_idle()
            return

        # Plot line with markers (stock-like)
        self.ax.plot(dff["Date"], dff["Price"], linewidth=2, marker="o")
        self.ax.set_title(f"{resource} � {unit} unit")
        self.ax.set_xlabel("Timestamp")
        self.ax.set_ylabel("Price")

        # Ticks & grid for readability
        self.ax.grid(True, linestyle="--", alpha=0.3)

        # Show last point as status
        last_ts = dff["Date"].iloc[-1]
        last_price = dff["Price"].iloc[-1]
        self.status.set(f"Last: {last_ts} ? {last_price}")

        # Tight layout and redraw
        self.fig.tight_layout()
        self.canvas.draw_idle()


def main():
    try:
        app = PriceGUI(CSV_FILE)
        app.mainloop()
    except Exception as e:
        messagebox = tk.messagebox if "tk" in globals() else None
        if messagebox:
            messagebox.showerror("Fatal Error", str(e))
        else:
            print("Fatal Error:", e)


if __name__ == "__main__":
    main()

