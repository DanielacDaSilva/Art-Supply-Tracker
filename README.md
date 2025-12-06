# Art Supply Tracker

## Overview
Art Supply Tracker is a Python desktop application built with Tkinter that allows artists to easily manage their art supplies. Users can add, update, and remove items, while keeping track of colors, brands, quantities, and optional sizes. The inventory can be saved to and loaded from a CSV file.

## Features
- Add and update items with quantity, color, brand, and optional size.
- Remove items from the inventory.
- Save the inventory to a CSV file.
- Load the inventory from a CSV file.
- Color-coded inventory display for easy visual reference.
- User-friendly graphical interface using Tkinter.
- Optional size selection for items.

## Inventory Management
The application keeps track of items in a structured inventory:
- **Item Name**
- **Color**
- **Brand**
- **Quantity**
- **Size (optional)**

Users can select an item, color, and brand to update the quantity, or add a new item with all details. Colors and sizes are customizable and can be added on the fly.

## Usage
1. Run the Python script: `tracker.py`.
2. Select an item, color, brand, and quantity.
3. Click **Add/Update** to save the changes.
4. To remove an item, select it and click **Remove**.
5. To add a completely new item, click **Add New Item**.
6. Save the current inventory to a CSV file using the **Save CSV** button.
7. The inventory will automatically load from `inventory.csv` if it exists when starting the app.

## Technologies
- Python 3
- Tkinter for GUI
- CSV for data storage

## Installation
1. Make sure Python 3 is installed.
2. Download or clone the project repository.
3. Run the script using Python:
   ```bash
   python tracker.py
```
