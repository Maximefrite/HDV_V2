#!/usr/bin/env python3
# plot_gui.py
# Local desktop GUI to explore expanded_prices_output.csv
# No web server, no internet.

import os
import re
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

import pandas as pd
import matplotlib
matplotlib.use("TkAgg")  # Tkinter backend
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk


CSV_FILE = "expanded_prices_output.csv"


def _parse_price_int(value):
    """
    Convert many common numeric formats to a non-negative *integer*.
    - Accepts floats/decimals and floors them (decimals are ignored).
    - Handles thousands separators: space, ',', '.'
    - Handles decimal separators: ',' or '.'
    - Removes currency symbols and other noise.
    - Returns pd.NA on failure or negatives.
    """
    # Fast-path for numeric types
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if pd.isna(value) or not math.isfinite(float(value)):
            return pd.NA
        if value < 0:
            return pd.NA
        return int(math.floor(float(value)))

    if pd.isna(value):
        return pd.NA

    s = str(value).strip()
    if not s:
        return pd.NA

    # Remove all non-digit/sep chars (keep digits and , . and spaces)
    s = re.sub(r"[^\d,.\s]", "", s)
    if not s:
        return pd.NA

    # Remove thin spaces / non-breaking spaces
    s = s.replace("\u00A0", "").replace("\u202F", "")
    # Strip regular spaces (assume thousands sep)
    s = s.replace(" ", "")

    # If both ',' and '.' appear, treat the *last* of them as decimal sep
    if "," in s and "." in s:
        last_idx = max(s.rfind(","), s.rfind("."))
        dec_char = s[last_idx]
        other = "," if dec_char == "." else "."
        s_clean = s.replace(other, "")
        s_clean = s_clean[:last_idx].replace(dec_char, "") + "." + s_clean[last_idx + 1:]
        s = s_clean
    else:
        # Only one of ',' or '.' present:
        if "," in s and "." not in s:
            s = s.replace(",", ".")

    # If there are multiple decimal points, keep the last as decimal; earlier are thousands
    if s.count(".") > 1:
        parts = s.split(".")
        s = "".join(parts[:-1]) + "." + parts[-1]

    try:
        val = float(s)
    except Exception:
        return pd.NA

    if not math.isfinite(val) or val < 0:
        return pd.NA

    return int(math.floor(val))


def load_long_df(csv_path: str) -> pd.DataFrame:
    """
    Load the wide CSV and convert to a tidy long dataframe:
    Input columns: Resource | YYYYMMDD_HHMMSS (one or more)
    Output columns: BaseResource | Unit | Date | Price (int or NA)
    """
    if not os.path.isfile(csv_path):
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    df = pd.read_csv(csv_path)

    if "Resource" not in df.columns:
        raise ValueError("CSV must contain a 'Resource' column.")

    # Melt wide -> long
    melted = df.melt(id_vars="Resource", var_name="Date", value_name="Price")

    # Extract unit from Resource like "Iron (10 unit)"; default to "1"
    melted["Unit"] = melted["Resource"].str.extract(r"\((\d+)\s*unit\)", expand=False)
    melted["Unit"] = melted["Unit"].fillna("1").astype(str)

    # Base name without "(x unit)"
    melted["BaseResource"] = (
        melted["Resource"]
        .str.replace(r"\s*\(\d+\s*unit\)\s*$", "", regex=True)
        .str.strip()
    )

    # Parse dates from column names (e.g., 20251027_142455). Fallback to pandas parsing.
    def parse_dt(x: str):
        if isinstance(x, str) and re.fullmatch(r"\d{8}_\d{6}", x):
            try:
                return pd.to_datetime(x, format="%Y%m%d_%H%M%S", utc=False)
            except Exception:
                return pd.NaT
        try:
            return pd.to_datetime(x, utc=False, infer_datetime_format=True)
        except Exception:
            return pd.NaT

    melted["Date"] = melted["Date"].map(parse_dt)

    # Integer-only price (decimals accepted but floored)
    melted["Price"] = melted["Price"].map(_parse_price_int)

    # Keep valid core fields; allow Price to be NA (skip at plot time)
    melted = melted.dropna(subset=["Date", "Unit", "BaseResource"])
    melted["Unit"] = melted["Unit"].astype(str)
    melted["BaseResource"] = melted["BaseResource"].astype(str)

    # Sort for nice plotting
    melted = melted.sort_values(["BaseResource", "Unit", "Date"]).reset_index(drop=True)
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

        # Unit dropdown (dynamic, includes "All")
        ttk.Label(ctrl, text="Unit:").pack(side=tk.LEFT, padx=(0, 6))
        self.unit_var = tk.StringVar()
        self.unit_cb = ttk.Combobox(ctrl, textvariable=self.unit_var, state="readonly", width=10)
        self.unit_cb.pack(side=tk.LEFT, padx=(0, 12))

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

        self.bind_events()
        self.populate_resources()
        self.update_units()
        self.update_plot(initial=True)

    def bind_events(self):
        self.resource_cb.bind("<<ComboboxSelected>>", lambda e: (self.update_units(), self.update_plot()))
        self.unit_cb.bind("<<ComboboxSelected>>", lambda e: self.update_plot())

    def populate_resources(self):
        resources = sorted(self.long_df["BaseResource"].unique()) if not self.long_df.empty else []
        self.resource_cb["values"] = resources
        if resources:
            current = self.resource_var.get()
            self.resource_cb.set(current if current in resources else resources[0])
        else:
            self.resource_cb.set("")

    def _units_for_resource(self, resource: str):
        if self.long_df.empty or not resource:
            return []
        units = sorted(
            self.long_df.loc[self.long_df["BaseResource"] == resource, "Unit"].unique(),
            key=lambda x: float(x) if re.fullmatch(r"\d+(\.\d+)?", str(x)) else float("inf"),
        )
        # ensure numeric-only units (regex earlier already yields digits), keep as strings
        return [u for u in units if re.fullmatch(r"\d+(\.\d+)?", str(u))]

    def update_units(self):
        """Populate unit options based on selected resource, including 'All'."""
        if self.long_df.empty:
            self.unit_cb["values"] = []
            self.unit_cb.set("")
            return

        resource = self.resource_var.get()
        units = self._units_for_resource(resource)

        all_plus_units = ["All"] + units if units else ["All"]
        self.unit_cb["values"] = all_plus_units

        current = self.unit_var.get()
        if current in all_plus_units:
            self.unit_cb.set(current)
        else:
            # default to "All" to show the comparison by default
            self.unit_cb.set("All")

    def refresh_csv(self):
        try:
            prev_res = self.resource_var.get()
            prev_unit = self.unit_var.get()

            self.long_df = load_long_df(self.csv_path)
            self.populate_resources()
            if prev_res in self.resource_cb["values"]:
                self.resource_cb.set(prev_res)
            self.update_units()
            if prev_unit in self.unit_cb["values"]:
                self.unit_cb.set(prev_unit)
            self.update_plot()
            self.status.set(f"Reloaded: {self.csv_path}")
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
                self.fig.savefig(path, bbox_inches="tight", dpi=150)
                self.status.set(f"Saved: {path}")
            except Exception as e:
                messagebox.showerror("Save Error", str(e))

    def update_plot(self, initial=False):
        self.ax.clear()

        if self.long_df.empty:
            self.ax.set_title("No data")
            self.status.set("No data")
            self.canvas.draw_idle()
            return

        resource = self.resource_var.get()
        if not resource and self.resource_cb["values"]:
            resource = self.resource_cb["values"][0]
            self.resource_cb.set(resource)

        unit_choice = self.unit_var.get()
        units_available = self._units_for_resource(resource)

        # Helper to filter and clean a unit's dataframe
        def df_for_unit(u: str) -> pd.DataFrame:
            dff = self.long_df[
                (self.long_df["BaseResource"] == resource) & (self.long_df["Unit"] == u)
            ].copy().sort_values("Date")
            return dff.dropna(subset=["Price"])

        if unit_choice == "All":
            # Plot each unit normalized per 1 unit (Price / unit_qty)
            any_plotted = False
            status_parts = []
            for u in units_available:
                dff_u = df_for_unit(u)
                if dff_u.empty:
                    continue
                try:
                    uq = float(u)
                    if uq <= 0:
                        continue
                except Exception:
                    continue

                y = dff_u["Price"] / uq  # per-1 normalization (may be fractional)
                self.ax.plot(dff_u["Date"], y, linewidth=2, marker="o", label=f"unit {u} (per 1)")
                any_plotted = True
                # last known per-unit value
                status_parts.append(f"{u}: {y.iloc[-1]:g}")

            if not any_plotted:
                self.ax.set_title(f"No data for: {resource}")
                self.ax.set_xlabel("Time")
                self.ax.set_ylabel("Price (per 1)")
                self.status.set("No data")
                self.canvas.draw_idle()
                return

            self.ax.set_title(f"{resource} � All units (per 1)")
            self.ax.set_xlabel("Timestamp")
            self.ax.set_ylabel("Price (per 1 unit)")
            self.ax.grid(True, linestyle="--", alpha=0.3)
            self.ax.legend(loc="best")

            self.status.set("Last per-1 ? " + " | ".join(status_parts))

        else:
            # Single unit view (raw integer prices; missing skipped)
            dff = self.long_df[
                (self.long_df["BaseResource"] == resource) & (self.long_df["Unit"] == unit_choice)
            ].copy().sort_values("Date")

            dff_valid = dff.dropna(subset=["Price"])
            if dff_valid.empty:
                self.ax.set_title(f"No data for: {resource} (unit {unit_choice})")
                self.ax.set_xlabel("Time")
                self.ax.set_ylabel("Price")
                self.status.set("No data")
                self.canvas.draw_idle()
                return

            self.ax.plot(dff_valid["Date"], dff_valid["Price"], linewidth=2, marker="o")
            self.ax.set_title(f"{resource} � unit {unit_choice}")
            self.ax.set_xlabel("Timestamp")
            self.ax.set_ylabel("Price")
            self.ax.grid(True, linestyle="--", alpha=0.3)

            last_ts = dff_valid["Date"].iloc[-1]
            last_price = int(dff_valid["Price"].iloc[-1])
            self.status.set(f"Last: {last_ts} ? {last_price}")

        self.fig.tight_layout()
        self.canvas.draw_idle()


def main():
    try:
        app = PriceGUI(CSV_FILE)
        app.mainloop()
    except Exception as e:
        try:
            messagebox.showerror("Fatal Error", str(e))
        except Exception:
            print("Fatal Error:", e)


if __name__ == "__main__":
    main()

