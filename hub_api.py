# UtilHub - Central Utility Dashboard
# Copyright (C) 2026 den89023
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

from gui import main_window
import datetime
import os
import time  # Нужно импортировать именно этот модуль

def hub_print(text, color="white"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    term_file = os.path.join("gui", "term.txt")
    with open(term_file, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] [COLOR:{color.lower()}]{text}[/COLOR]\n")

def hub_input():
    input_file = os.path.join("gui", "input.txt")
    
    if os.path.exists(input_file):
        os.remove(input_file)
    
    while not os.path.exists(input_file):
        time.sleep(0.1)  # Использовать модуль time
    
    with open(input_file, "r", encoding="utf-8") as f:
        text = f.read().strip()
    
    if os.path.exists(input_file):
        os.remove(input_file)
    
    return text