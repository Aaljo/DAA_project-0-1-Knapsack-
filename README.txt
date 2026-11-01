Emergency Supply Selection System - 0/1 Knapsack
=================================================

Files
-----
gui.py             Tkinter GUI
knapsack.py        0/1 Knapsack dynamic-programming implementation
test_button.py     Automated GUI button and handler tests
requirements.txt   Python dependencies

Run the application
-------------------
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Install dependencies:
       python -m pip install -r requirements.txt
4. Start the application:
       python gui.py

Edit a supply
-------------
1. Select a row in the Available Supplies table.
2. Click Edit Selected. Its values are loaded into the form.
3. Change the name, weight and/or priority.
4. Click Save Changes.
5. Click Cancel Edit to discard an edit instead.

Run automated tests
-------------------
Run from a desktop session (Tkinter needs a display):
       python test_button.py

The tests invoke the actual GUI buttons and check adding, editing, saving,
cancelling, removing, clearing, loading sample data, setting capacity,
running the algorithm, generating/refreshing the chart, and showing steps.
