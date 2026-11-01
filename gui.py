"""
Emergency Supply Selection System - GUI Application
0/1 Knapsack Algorithm based DAA Project
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from knapsack import Supply, KnapsackSolver


class SupplyManager:
    """Manages the list of emergency supplies."""

    def __init__(self):
        self.supplies: list[Supply] = []

    def add(self, name: str, weight: int, priority: int) -> None:
        """Add a new supply."""
        if not name.strip():
            raise ValueError("Supply name cannot be empty")
        supply = Supply(name.strip(), weight, priority)
        self.supplies.append(supply)

    def remove(self, index: int) -> None:
        """Remove supply at given index."""
        if index < 0 or index >= len(self.supplies):
            raise IndexError("Invalid supply index")
        del self.supplies[index]

    def update(self, index: int, name: str, weight: int, priority: int) -> None:
        """Update supply at given index."""
        if index < 0 or index >= len(self.supplies):
            raise IndexError("Invalid supply index")
        if not name.strip():
            raise ValueError("Supply name cannot be empty")
        self.supplies[index] = Supply(name.strip(), weight, priority)

    def get_all(self) -> list[Supply]:
        """Get all supplies."""
        return list(self.supplies)

    def clear(self) -> None:
        """Clear all supplies."""
        self.supplies.clear()


# Default fake dataset to demonstrate the application working
FAKE_DATASET = [
    ("First-aid kit", 5, 10),
    ("Food packets", 8, 12),
    ("Water bottles", 6, 8),
    ("Emergency medicine", 3, 9),
    ("Blanket", 7, 7),
    ("Flashlight", 2, 6),
    ("Tent", 9, 5),
    ("Multi-tool", 1, 8),
    ("Rope", 4, 7),
    ("Emergency beacon", 1, 10),
]


class KnapsackGUI:
    """Main GUI application for Emergency Supply Selection System."""

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Emergency Supply Selection System - 0/1 Knapsack")
        self.root.geometry("1100x800")
        self.root.minsize(900, 700)

        # Configure style for modern look
        self._setup_styles()

        self.manager = SupplyManager()
        self.solver = KnapsackSolver()
        self.capacity_var = tk.StringVar(value="20")
        self._editing_index = None

        # Build layout first so all widgets (treeview, listboxes, etc.) exist
        self._build_layout()

        # Load fake data automatically to demonstrate the app working
        self._load_fake_data()

    def _setup_styles(self):
        """Configure ttk styles for modern appearance."""
        style = ttk.Style()
        style.theme_use("clam")

        # Modern color palette (stored as instance attrs so other methods can use them)
        self.primary_color = "#2c3e50"      # Dark navy for headers
        self.accent_color = "#3498db"       # Bright blue for accents
        self.success_color = "#27ae60"      # Green for success
        self.warning_color = "#e67e22"      # Orange for warnings
        self.error_color = "#e74c3c"        # Red for errors
        self.light_bg = "#f8f9fa"           # Light background
        self.card_bg = "#ffffff"            # Card/white background
        self.text_color = "#2c3e50"         # Body text color

        # Give the root window a colorful gradient-like background
        self.root.configure(bg="#eef2f7")

        self.panel_bg = "#eaf1fb"
        self.root.configure(bg=self.panel_bg)
        style.configure("TFrame", background=self.panel_bg)
        style.configure("Card.TFrame", background="#ffffff")
        style.configure("TLabel", background=self.panel_bg, foreground=self.text_color, font=("Segoe UI", 10))
        style.configure("Title.TLabel", background=self.panel_bg, font=("Segoe UI", 19, "bold"), foreground=self.primary_color)
        style.configure("Subtitle.TLabel", background=self.panel_bg, font=("Segoe UI", 13, "bold"), foreground=self.primary_color)
        style.configure("Body.TLabel", background=self.panel_bg, font=("Segoe UI", 10), foreground=self.text_color)
        style.configure("TLabelframe", background=self.panel_bg, bordercolor="#cbd5e1")
        style.configure("TLabelframe.Label", background=self.panel_bg, foreground=self.primary_color, font=("Segoe UI", 10, "bold"))
        style.configure("TNotebook", background=self.panel_bg, borderwidth=0)
        style.configure("TNotebook.Tab", padding=(16, 9), font=("Segoe UI", 10, "bold"), background="#dbeafe", foreground=self.primary_color)
        style.map("TNotebook.Tab", background=[("selected", self.accent_color)], foreground=[("selected", "white")])
        style.configure("Treeview", rowheight=30, background="#ffffff", fieldbackground="#ffffff", foreground=self.text_color, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.primary_color, foreground="white", padding=7)
        style.map("Treeview", background=[("selected", "#bfdbfe")], foreground=[("selected", self.primary_color)])
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background=self.accent_color, foreground="white", padding=(12, 8))
        style.map("Accent.TButton", background=[("active", "#2563eb")])
        style.configure("Success.TButton", font=("Segoe UI", 10, "bold"), background=self.success_color, foreground="white", padding=(14, 9))
        style.map("Success.TButton", background=[("active", "#15803d")])
        style.configure("Warning.TButton", font=("Segoe UI", 10, "bold"), background=self.warning_color, foreground="white")

    def _build_layout(self):
        """Build the main UI layout."""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding=20, style="Card.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Title area
        self._create_title_area(main_frame)

        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Tab 1: Supply Management
        self.tab_supply = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_supply, text="📦 Manage Supplies")
        self._build_supply_tab()

        # Tab 2: Knapsack Settings & Results
        self.tab_knapsack = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_knapsack, text="⚙️ Knapsack & Results")
        self._build_knapsack_tab()

        # Tab 3: Visualization
        self.tab_viz = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_viz, text="📊 Visualization")
        self._build_viz_tab()

        # Tab 4: Step-by-Step
        self.tab_steps = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_steps, text="📋 Algorithm Steps")
        self._build_steps_tab()

    def _create_title_area(self, parent):
        """Create the application title area."""
        title_frame = ttk.Frame(parent)
        title_frame.pack(fill=tk.X, pady=(0, 20))

        ttk.Label(title_frame, text="Emergency Supply Selection System", style="Title.TLabel").pack(side=tk.LEFT)
        ttk.Label(title_frame, text="0/1 Knapsack Algorithm", style="Body.TLabel").pack(side=tk.LEFT, padx=(10, 0))

    # ==================== TAB 1: SUPPLY MANAGEMENT ====================

    def _build_supply_tab(self):
        """Build the supply management tab."""
        frame = self.tab_supply

        # Title
        ttk.Label(frame, text="Emergency Supplies Management", style="Title.TLabel").pack(pady=(15, 10))

        # Input form with card-like feel
        form_frame = ttk.LabelFrame(frame, text="Add / Edit Supply", padding=15)
        form_frame.pack(fill=tk.X, padx=20, pady=10)

        # Name
        ttk.Label(form_frame, text="Supply Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.entry_name = ttk.Entry(form_frame, width=30)
        self.entry_name.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Weight
        ttk.Label(form_frame, text="Weight (kg):").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_weight = ttk.Entry(form_frame, width=15)
        self.entry_weight.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Priority
        ttk.Label(form_frame, text="Priority Value:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_priority = ttk.Entry(form_frame, width=15)
        self.entry_priority.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Buttons with modern styling
        btn_frame = ttk.Frame(form_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=15)

        self.add_button = ttk.Button(btn_frame, text="Add Supply", command=self._on_add, style="Accent.TButton")
        self.add_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Selected", command=self._on_edit).pack(side=tk.LEFT, padx=5)
        self.update_button = ttk.Button(btn_frame, text="Save Changes", command=self._on_update, state=tk.DISABLED, style="Success.TButton")
        self.update_button.pack(side=tk.LEFT, padx=5)
        self.cancel_edit_button = ttk.Button(btn_frame, text="Cancel Edit", command=self._on_cancel_edit, state=tk.DISABLED)
        self.cancel_edit_button.pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Remove Selected", command=self._on_remove).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear All", command=self._on_clear).pack(side=tk.LEFT, padx=5)

        # Supplies table with improved styling
        table_frame = ttk.LabelFrame(frame, text="Available Supplies", padding=10)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        columns = ("#", "Supply Name", "Weight (kg)", "Priority Value")
        self.supply_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=12)

        self.supply_tree.heading("#", text="#")
        self.supply_tree.heading("Supply Name", text="Supply Name")
        self.supply_tree.heading("Weight (kg)", text="Weight (kg)")
        self.supply_tree.heading("Priority Value", text="Priority Value")

        self.supply_tree.column("#", width=50, anchor=tk.CENTER)
        self.supply_tree.column("Supply Name", width=250, anchor=tk.W)
        self.supply_tree.column("Weight (kg)", width=150, anchor=tk.CENTER)
        self.supply_tree.column("Priority Value", width=150, anchor=tk.CENTER)

        self.supply_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.supply_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.supply_tree.configure(yscrollcommand=scrollbar.set)

        # Load sample data button - now loads fake dataset
        btn_sample = ttk.Button(frame, text="Load Fake Data", command=self._load_fake_data)
        btn_sample.pack(pady=10)

    # ==================== TAB 2: KNAPSACK & RESULTS ====================

    def _build_knapsack_tab(self):
        """Build the knapsack settings and results tab."""
        frame = self.tab_knapsack

        # Title
        ttk.Label(frame, text="0/1 Knapsack Optimization", style="Title.TLabel").pack(pady=(15, 10))

        # Capacity setting
        cap_frame = ttk.LabelFrame(frame, text="Vehicle Capacity", padding=15)
        cap_frame.pack(fill=tk.X, padx=20, pady=10)

        ttk.Label(cap_frame, text="Maximum Capacity (kg):").pack(side=tk.LEFT, padx=(0, 10))
        self.entry_capacity = ttk.Entry(cap_frame, width=10, textvariable=self.capacity_var)
        self.entry_capacity.pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(cap_frame, text="Set Capacity", command=self._on_set_capacity).pack(side=tk.LEFT, padx=5)
        self.run_button = ttk.Button(
            cap_frame,
            text="▶  Run Knapsack Algorithm",
            command=self._on_run_knapsack,
            style="Success.TButton"
        )
        self.run_button.pack(side=tk.LEFT, padx=10)

        # Results display
        result_frame = ttk.LabelFrame(frame, text="Results", padding=15)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Left: Selected items
        left_frame = ttk.Frame(result_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        ttk.Label(left_frame, text="Selected Supplies", font=("Segoe UI", 12, "bold")).pack(pady=(0, 5))
        # Colorful listbox with accent color highlight
        self.selected_listbox = tk.Listbox(left_frame, height=10, font=("Consolas", 11), bg="#ecfdf5", fg="#166534", selectbackground=self.success_color, selectforeground="white", relief=tk.FLAT, highlightthickness=1, highlightbackground="#bbf7d0")
        self.selected_listbox.pack(fill=tk.BOTH, expand=True)

        # Right: Rejected items
        right_frame = ttk.Frame(result_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))

        ttk.Label(right_frame, text="Rejected Supplies", font=("Segoe UI", 12, "bold")).pack(pady=(0, 5))
        # Colorful listbox with accent color highlight
        self.rejected_listbox = tk.Listbox(right_frame, height=10, font=("Consolas", 11), bg="#fff1f2", fg="#9f1239", selectbackground=self.error_color, selectforeground="white", relief=tk.FLAT, highlightthickness=1, highlightbackground="#fecdd3")
        self.rejected_listbox.pack(fill=tk.BOTH, expand=True)

        # Summary
        summary_frame = ttk.Frame(frame)
        summary_frame.pack(fill=tk.X, padx=20, pady=15)

        self.label_total_weight = ttk.Label(summary_frame, text="Total Weight: 0 kg", font=("Segoe UI", 11, "bold"))
        self.label_total_weight.pack(side=tk.LEFT, padx=20)

        self.label_total_priority = ttk.Label(summary_frame, text="Total Priority: 0", font=("Segoe UI", 11, "bold"))
        self.label_total_priority.pack(side=tk.LEFT, padx=20)

        self.label_remaining = ttk.Label(summary_frame, text="Remaining Capacity: 0 kg", font=("Segoe UI", 11, "bold"))
        self.label_remaining.pack(side=tk.LEFT, padx=20)

    # ==================== TAB 3: VISUALIZATION ====================

    def _build_viz_tab(self):
        """Build the visualization tab."""
        frame = self.tab_viz

        ttk.Label(frame, text="Supply Visualization", style="Title.TLabel").pack(pady=(15, 10))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Generate Chart", command=self._on_generate_chart, style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh Chart", command=self._on_generate_chart).pack(side=tk.LEFT, padx=5)

        # Chart container
        self.chart_frame = ttk.Frame(frame)
        self.chart_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.chart_canvas = None
        self.chart_toolbar = None

    # ==================== TAB 4: STEP-BY-STEP ====================

    def _build_steps_tab(self):
        """Build the step-by-step algorithm execution tab."""
        frame = self.tab_steps

        ttk.Label(frame, text="Step-by-Step Algorithm Execution", style="Title.TLabel").pack(pady=(15, 10))

        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Show Algorithm Steps", command=self._on_show_steps, style="Accent.TButton").pack(side=tk.LEFT, padx=5)

        # Text area for steps
        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.steps_text = tk.Text(text_frame, font=("Consolas", 10), wrap=tk.WORD, bg="white", fg=self.primary_color)
        self.steps_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.steps_text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.steps_text.configure(yscrollcommand=scrollbar.set)

    # ==================== ACTIONS ====================

    def _refresh_table(self):
        """Refresh the supplies table and keep the edited row selected."""
        for item in self.supply_tree.get_children():
            self.supply_tree.delete(item)

        selected_iid = None
        for i, supply in enumerate(self.manager.get_all(), start=1):
            iid = self.supply_tree.insert("", tk.END, values=(i, supply.name, supply.weight, supply.priority))
            if self._editing_index == i - 1:
                selected_iid = iid
        if selected_iid:
            self.supply_tree.selection_set(selected_iid)
            self.supply_tree.focus(selected_iid)

    def _get_selected_tree_index(self) -> int:
        """Get the index of the selected item in the tree."""
        selection = self.supply_tree.selection()
        if not selection:
            return -1
        item = self.supply_tree.item(selection[0])
        values = item["values"]
        return int(values[0]) - 1  # Convert the displayed 1-based row number to a 0-based index.

    def _read_supply_form(self):
        """Read and validate the supply form without changing stored data."""
        name = self.entry_name.get().strip()
        if not name:
            raise ValueError("Supply name cannot be empty.")
        try:
            weight = int(self.entry_weight.get().strip())
            priority = int(self.entry_priority.get().strip())
        except ValueError:
            raise ValueError("Weight and priority must be whole numbers.")
        if weight < 0 or priority < 0:
            raise ValueError("Weight and priority cannot be negative.")
        return name, weight, priority

    def _clear_supply_form(self):
        for entry in (self.entry_name, self.entry_weight, self.entry_priority):
            entry.delete(0, tk.END)

    def _set_edit_mode(self, enabled):
        self._editing_index = self._editing_index if enabled else None
        self.add_button.configure(state=tk.DISABLED if enabled else tk.NORMAL)
        self.update_button.configure(state=tk.NORMAL if enabled else tk.DISABLED)
        self.cancel_edit_button.configure(state=tk.NORMAL if enabled else tk.DISABLED)

    def _on_add(self):
        """Add a new supply after validating all fields."""
        if self._editing_index is not None:
            messagebox.showwarning("Edit in Progress", "Save or cancel the current edit before adding another supply.")
            return
        try:
            name, weight, priority = self._read_supply_form()
            self.manager.add(name, weight, priority)
            self._refresh_table()
            self._clear_supply_form()
            messagebox.showinfo("Success", f"Supply '{name}' added successfully!")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _on_edit(self):
        """Load the selected supply into the form for editing; do not save yet."""
        index = self._get_selected_tree_index()
        if index == -1:
            messagebox.showwarning("Selection Required", "Please select a supply to edit.")
            return
        if index >= len(self.manager.get_all()):
            messagebox.showerror("Edit Error", "The selected supply no longer exists. Refresh the table and try again.")
            return

        supply = self.manager.get_all()[index]
        self._clear_supply_form()
        self.entry_name.insert(0, supply.name)
        self.entry_weight.insert(0, str(supply.weight))
        self.entry_priority.insert(0, str(supply.priority))
        self._editing_index = index
        self._set_edit_mode(True)
        self.entry_name.focus_set()

    def _on_update(self):
        """Save changes to the supply currently being edited."""
        if self._editing_index is None:
            messagebox.showwarning("No Active Edit", "Click Edit Selected before saving changes.")
            return
        try:
            name, weight, priority = self._read_supply_form()
            self.manager.update(self._editing_index, name, weight, priority)
            self._refresh_table()
            self._clear_supply_form()
            self._set_edit_mode(False)
            messagebox.showinfo("Updated", f"Supply '{name}' updated successfully.")
        except ValueError as e:
            messagebox.showerror("Input Error", str(e))

    def _on_cancel_edit(self):
        """Discard form changes and leave edit mode."""
        if self._editing_index is None:
            return
        self._clear_supply_form()
        self._set_edit_mode(False)

    def _on_remove(self):
        """Handle Remove Selected button."""
        index = self._get_selected_tree_index()
        if index == -1:
            messagebox.showwarning("Selection Required", "Please select a supply to remove.")
            return

        supplies = self.manager.get_all()
        name = supplies[index].name

        if messagebox.askyesno("Confirm Remove", f"Remove supply '{name}'?"):
            self.manager.remove(index)
            if self._editing_index == index:
                self._on_cancel_edit()
            elif self._editing_index is not None and self._editing_index > index:
                self._editing_index -= 1
            self._refresh_table()

    def _on_clear(self):
        """Handle Clear All button."""
        if not self.manager.get_all():
            return
        if messagebox.askyesno("Confirm Clear", "Clear all supplies?"):
            self.manager.clear()
            self._on_cancel_edit()
            self._refresh_table()
            self._clear_result_lists()

    def _clear_result_lists(self):
        """Clear stale result lists and summary labels after data changes."""
        self.selected_listbox.delete(0, tk.END)
        self.rejected_listbox.delete(0, tk.END)
        self.label_total_weight.config(text="Total Weight: 0 kg")
        self.label_total_priority.config(text="Total Priority: 0")
        self.label_remaining.config(text="Remaining Capacity: 0 kg")

    def _load_fake_data(self):
        """Load the fake dataset to demonstrate the app working."""
        self.manager.clear()
        self._on_cancel_edit()
        for name, weight, priority in FAKE_DATASET:
            self.manager.add(name, weight, priority)

        self._refresh_table()
        # Auto-set capacity to a reasonable default.
        total_weight = sum(w for _, w, _ in FAKE_DATASET)
        if total_weight > 0:
            max_cap = total_weight + 5  # Give some extra capacity
            self.entry_capacity.delete(0, tk.END)
            self.entry_capacity.insert(0, str(max_cap))
            self.capacity_var.set(str(max_cap))

        # Auto-run knapsack to show it works
        self._on_run_knapsack()

        # Auto-generate chart
        self._on_generate_chart()

        messagebox.showinfo("Fake Data Loaded",
                           f"Fake emergency supplies dataset loaded successfully!\n\n"
                           f"{len(FAKE_DATASET)} supplies added with total weight {sum(w for _, w, _ in FAKE_DATASET)}kg.\n"
                           f"The knapsack algorithm has been run and visualization generated to demonstrate the app working.")

    def _on_set_capacity(self):
        """Handle Set Capacity button."""
        try:
            capacity = int(self.entry_capacity.get().strip() or 0)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a valid number.")
            return
        if capacity <= 0:
            messagebox.showwarning("Invalid Capacity", "Capacity must be greater than 0 kg.")
            return
        self.capacity_var.set(str(capacity))
        self.solver.set_capacity(capacity)
        messagebox.showinfo("Capacity Set", f"Maximum capacity set to {capacity} kg")

    def _on_run_knapsack(self):
        """Handle Run Knapsack Algorithm button."""
        supplies = self.manager.get_all()
        if not supplies:
            messagebox.showwarning("No Supplies", "Please add some supplies first.")
            return

        try:
            capacity = int(self.entry_capacity.get().strip() or 0)
        except ValueError:
            messagebox.showerror("Error", "Capacity must be a valid number.")
            return
        if capacity <= 0:
            messagebox.showwarning("Invalid Capacity", "Please set a valid capacity greater than 0.")
            return

        self.solver.set_supplies(supplies)
        self.capacity_var.set(str(capacity))
        self.solver.set_capacity(capacity)

        try:
            result = self.solver.solve()
            self._display_results(result)

            # Switch to results tab
            self.notebook.select(self.tab_knapsack)

        except Exception as e:
            messagebox.showerror("Algorithm Error", str(e))

    def _display_results(self, result):
        """Display knapsack results."""
        # Clear listboxes
        self.selected_listbox.delete(0, tk.END)
        self.rejected_listbox.delete(0, tk.END)

        # Use object identity rather than names so duplicate supply names are handled correctly.
        selected_item_ids = {id(item) for item in result.selected_items}
        all_supplies = self.manager.get_all()

        # Populate selected items
        for item in result.selected_items:
            self.selected_listbox.insert(
                tk.END,
                f"{item.name:25s} | {item.weight:3d} kg  | Priority: {item.priority}"
            )

        # Populate rejected items
        for item in all_supplies:
            if id(item) not in selected_item_ids:
                self.rejected_listbox.insert(
                    tk.END,
                    f"{item.name:25s} | {item.weight:3d} kg  | Priority: {item.priority}"
                )

        # Update summary
        capacity = self.solver.capacity
        self.label_total_weight.config(text=f"Total Weight: {result.total_weight} kg / {capacity} kg")
        self.label_total_priority.config(text=f"Total Priority: {result.total_priority}")
        remaining = capacity - result.total_weight
        self.label_remaining.config(text=f"Remaining Capacity: {remaining} kg")

    def _on_generate_chart(self):
        """Generate visualization chart."""
        # Clear previous chart and release its Matplotlib figure.
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        if self.chart_canvas is not None:
            old_figure = self.chart_canvas.figure
            plt.close(old_figure)
            self.chart_canvas = None
            self.chart_toolbar = None

        supplies = self.manager.get_all()
        if not supplies:
            messagebox.showwarning("No Supplies", "Please add supplies first to visualize.")
            return

        # Create figure with modern styling
        fig, ax = plt.subplots(figsize=(10, 6), facecolor="#f8f9fa")
        ax.set_facecolor("#f8f9fa")

        names = [s.name for s in supplies]
        weights = [s.weight for s in supplies]
        priorities = [s.priority for s in supplies]

        x = range(len(names))
        width = 0.35

        # Use modern colors
        bars1 = ax.bar([i - width/2 for i in x], weights, width, label='Weight (kg)', color='#3498db', alpha=0.85, edgecolor='white')
        bars2 = ax.bar([i + width/2 for i in x], priorities, width, label='Priority Value', color='#e74c3c', alpha=0.85, edgecolor='white')

        ax.set_xlabel('Supplies', fontsize=11, color=self.primary_color)
        ax.set_ylabel('Value', fontsize=11, color=self.primary_color)
        ax.set_title('Emergency Supplies - Weight vs Priority', fontsize=14, fontweight='bold', color=self.primary_color, pad=15)
        ax.set_xticks(x)
        ax.set_xticklabels(names, rotation=45, ha='right', fontsize=9)
        ax.legend(fontsize=10, loc='upper right')
        ax.grid(axis='y', alpha=0.3, color='gray')
        ax.tick_params(axis='x', colors=self.primary_color)
        ax.tick_params(axis='y', colors=self.primary_color)

        plt.tight_layout()

        # Embed in Tkinter
        self.chart_canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.chart_canvas.draw()
        self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        # Add toolbar
        self.chart_toolbar = NavigationToolbar2Tk(self.chart_canvas, self.chart_frame)
        self.chart_toolbar.update()
        self.chart_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

    def _on_show_steps(self):
        """Show step-by-step algorithm execution."""
        supplies = self.manager.get_all()
        if not supplies:
            messagebox.showwarning("No Supplies", "Please add supplies first.")
            return

        try:
            capacity = int(self.entry_capacity.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Capacity", "Enter a whole-number capacity.")
            return
        if capacity <= 0:
            messagebox.showwarning("Invalid Capacity", "Please set a valid capacity greater than 0.")
            return

        self.capacity_var.set(str(capacity))
        self.solver.set_supplies(supplies)
        self.solver.set_capacity(capacity)

        try:
            result = self.solver.solve()
            steps = self.solver.get_step_by_step_explanation(result)

            self.steps_text.delete("1.0", tk.END)
            self.steps_text.insert("1.0", "\n".join(steps))

            self.notebook.select(self.tab_steps)

        except Exception as e:
            messagebox.showerror("Algorithm Error", str(e))


def main():
    root = tk.Tk()
    app = KnapsackGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()