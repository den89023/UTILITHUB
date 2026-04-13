# UtilHub - Central Utility Dashboard
# UTILITHUB
![UtilHub Logo](logo.png)
A GUI application for running utility scripts with a terminal-like output interface.

## Features

- **Script Execution**: Run Python scripts from the `scripts/` directory using START button
- **Process Control**: Start and stop scripts with START/STOP buttons
- **Terminal Output**: View script output in a read-only terminal with timestamps and color-coded messages
- **Manual Input**: Add custom text to the terminal
- **Clear Terminal**: Reset terminal to initial state
- **Real-time Updates**: Terminal updates automatically every 100ms

## Requirements

- Python 3.6+
- CustomTkinter: `pip install customtkinter`

## Installation

1. Clone or download the repository
2. Install dependencies: `pip install customtkinter`
3. Run: `python main.py`

## Usage

1. Select a script from the dropdown menu
2. Click "START" to run the selected script
3. Click "STOP" to terminate the running script
4. Use "Write to Terminal" to add custom messages
5. Use "CLEAR" to reset the terminal

Scripts output colored messages using `hub_print(text, color)` where color can be "red", "green", "yellow", "blue", or "white".

## Script Development

Scripts should use `hub_print(text, color)` from `hub_api.py` to output to the terminal.

Available colors: "red", "green", "yellow", "blue", "white"

Example:
```python
from hub_api import hub_print

hub_print("Hello World!", "green")
```

## Project Structure

- `main.py`: Entry point
- `gui/main_window.py`: Main GUI application
- `core/file_manager.py`: Script listing functionality
- `core/executor.py`: Script execution (legacy)
- `hub_api.py`: Logging API for scripts
- `scripts/`: Directory containing utility scripts

## License

GNU GPL v3
