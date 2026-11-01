"""Automated GUI-handler tests for the Emergency Supply Knapsack project.

Run on Windows with: python test_button.py
The test creates a real Tk window, so a desktop session is required.
"""
import tkinter as tk
from tkinter import messagebox
import unittest

from gui import KnapsackGUI, FAKE_DATASET


class KnapsackButtonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Prevent modal dialogs from blocking automated tests.
        cls._showinfo = messagebox.showinfo
        cls._showwarning = messagebox.showwarning
        cls._showerror = messagebox.showerror
        cls._askyesno = messagebox.askyesno
        messagebox.showinfo = lambda *a, **k: None
        messagebox.showwarning = lambda *a, **k: None
        messagebox.showerror = lambda *a, **k: None
        messagebox.askyesno = lambda *a, **k: True

    @classmethod
    def tearDownClass(cls):
        messagebox.showinfo = cls._showinfo
        messagebox.showwarning = cls._showwarning
        messagebox.showerror = cls._showerror
        messagebox.askyesno = cls._askyesno

    def setUp(self):
        self.root = tk.Tk()
        self.app = KnapsackGUI(self.root)
        self.root.update_idletasks()

    def tearDown(self):
        self.root.destroy()

    def fill_form(self, name, weight, priority):
        self.app._clear_supply_form()
        self.app.entry_name.insert(0, name)
        self.app.entry_weight.insert(0, str(weight))
        self.app.entry_priority.insert(0, str(priority))

    def select_row(self, index):
        children = self.app.supply_tree.get_children()
        self.app.supply_tree.selection_set(children[index])
        self.app.supply_tree.focus(children[index])

    def test_add_supply(self):
        before = len(self.app.manager.get_all())
        self.fill_form("Test supply", 2, 9)
        self.app._on_add()
        self.assertEqual(len(self.app.manager.get_all()), before + 1)
        self.assertEqual(self.app.manager.get_all()[-1].name, "Test supply")

    def test_edit_selected_requires_save_and_updates_record(self):
        original = self.app.manager.get_all()[0]
        self.select_row(0)
        self.app._on_edit()
        self.assertEqual(self.app.entry_name.get(), original.name)
        self.assertIsNotNone(self.app._editing_index)
        self.fill_form("Edited first aid", 4, 15)
        self.app._on_update()
        updated = self.app.manager.get_all()[0]
        self.assertEqual((updated.name, updated.weight, updated.priority), ("Edited first aid", 4, 15))
        self.assertIsNone(self.app._editing_index)

    def test_invalid_edit_does_not_modify_existing_record(self):
        original = self.app.manager.get_all()[0]
        self.select_row(0)
        self.app._on_edit()
        self.fill_form("Broken edit", "not-a-number", 12)
        self.app._on_update()
        unchanged = self.app.manager.get_all()[0]
        self.assertEqual((unchanged.name, unchanged.weight, unchanged.priority),
                         (original.name, original.weight, original.priority))
        self.assertIsNotNone(self.app._editing_index)

    def test_cancel_edit_discards_form(self):
        self.select_row(0)
        self.app._on_edit()
        self.fill_form("Discard me", 1, 1)
        self.app._on_cancel_edit()
        self.assertIsNone(self.app._editing_index)
        self.assertEqual(self.app.entry_name.get(), "")

    def test_remove_selected(self):
        before = len(self.app.manager.get_all())
        self.select_row(0)
        self.app._on_remove()
        self.assertEqual(len(self.app.manager.get_all()), before - 1)

    def test_clear_all(self):
        self.app._on_clear()
        self.assertEqual(len(self.app.manager.get_all()), 0)
        self.assertEqual(self.app.supply_tree.get_children(), ())

    def test_load_fake_data(self):
        self.app.manager.clear()
        self.app._refresh_table()
        self.app._load_fake_data()
        self.assertEqual(len(self.app.manager.get_all()), len(FAKE_DATASET))

    def test_set_capacity_and_run_knapsack(self):
        self.app.entry_capacity.delete(0, tk.END)
        self.app.entry_capacity.insert(0, "20")
        self.app._on_set_capacity()
        self.app._on_run_knapsack()
        self.assertGreater(self.app.selected_listbox.size(), 0)
        self.assertEqual(self.app.solver.capacity, 20)
        self.assertIn("/ 20 kg", self.app.label_total_weight.cget("text"))

    def test_generate_chart(self):
        self.app._on_generate_chart()
        self.root.update_idletasks()
        self.assertIsNotNone(self.app.chart_canvas)
        self.assertTrue(self.app.chart_canvas.get_tk_widget().winfo_exists())


    def _find_button(self, text):
        def walk(widget):
            for child in widget.winfo_children():
                if isinstance(child, (tk.Button,)) or child.winfo_class() == "TButton":
                    if child.cget("text") == text:
                        return child
                found = walk(child)
                if found:
                    return found
            return None
        button = walk(self.root)
        self.assertIsNotNone(button, f"Button not found: {text}")
        self.assertTrue(button.cget("command"), f"Button has no command: {text}")
        return button

    def test_actual_button_widgets_end_to_end(self):
        """Invoke the actual visible buttons, not just their handler methods."""
        # Add Supply
        self.fill_form("Button-added item", 2, 5)
        self._find_button("Add Supply").invoke()
        self.assertEqual(self.app.manager.get_all()[-1].name, "Button-added item")

        # Edit Selected -> Save Changes
        self.select_row(0)
        self._find_button("Edit Selected").invoke()
        self.fill_form("Button-edited item", 3, 11)
        self._find_button("Save Changes").invoke()
        self.assertEqual(self.app.manager.get_all()[0].name, "Button-edited item")

        # Edit Selected -> Cancel Edit
        self.select_row(0)
        self._find_button("Edit Selected").invoke()
        self._find_button("Cancel Edit").invoke()
        self.assertIsNone(self.app._editing_index)

        # Remove Selected and Clear All
        self.select_row(0)
        before = len(self.app.manager.get_all())
        self._find_button("Remove Selected").invoke()
        self.assertEqual(len(self.app.manager.get_all()), before - 1)
        self._find_button("Clear All").invoke()
        self.assertEqual(len(self.app.manager.get_all()), 0)

        # Load data, set capacity, solve, chart actions, and algorithm explanation
        self._find_button("Load Fake Data").invoke()
        self.assertEqual(len(self.app.manager.get_all()), len(FAKE_DATASET))
        self.app.entry_capacity.delete(0, tk.END)
        self.app.entry_capacity.insert(0, "20")
        self._find_button("Set Capacity").invoke()
        self.app.run_button.invoke()
        self.assertGreater(self.app.selected_listbox.size(), 0)
        self._find_button("Generate Chart").invoke()
        self.assertIsNotNone(self.app.chart_canvas)
        self._find_button("Refresh Chart").invoke()
        self.assertIsNotNone(self.app.chart_canvas)
        self._find_button("Show Algorithm Steps").invoke()
        self.assertIn("FINAL RESULT", self.app.steps_text.get("1.0", tk.END))

    def test_show_algorithm_steps(self):
        self.app._on_show_steps()
        content = self.app.steps_text.get("1.0", tk.END)
        self.assertIn("0/1 KNAPSACK ALGORITHM", content)
        self.assertIn("FINAL RESULT", content)


if __name__ == "__main__":
    unittest.main(verbosity=2)
