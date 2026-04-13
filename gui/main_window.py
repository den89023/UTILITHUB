# UtilHub - Central Utility Dashboard
# Copyright (C) 2026 den89023
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

from pydoc import text

import customtkinter as ctk
import tkinter as tk
import os
import subprocess
import threading
import sys

current_process = None

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.file_manager import get_scripts_list

def start_app():
    global current_process
    root = ctk.CTk()
    root.title("UtilHub v0.1")
    root.geometry("900x650")
    
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(3, weight=1)

    ascii_art = """╔══════════════════════════════════════════╗
║                UTILHUB                   ║
╟──────────────────────────────────────────╢
║  Author: den89023                        ║
║  Year: 2026                              ║
║  License: GNU GPL v3 (since 2007)        ║
╚══════════════════════════════════════════╝

"""

    # 5. Terminal
    terminal_frame = ctk.CTkFrame(root, corner_radius=10)
    terminal_frame.grid(row=4, column=0, padx=20, pady=(5, 15), sticky="nsew")
    terminal_frame.grid_columnconfigure(0, weight=1)
    terminal_frame.grid_rowconfigure(0, weight=1)
    
    terminal_text = tk.Text(terminal_frame, width=80, height=15, font=("Consolas", 12), 
                            bg="#1E1E1E", fg="#F1C40F", insertbackground="#F1C40F",
                            wrap=tk.WORD, state="disabled")
    terminal_text.grid(row=0, column=0, sticky="nsew")
    
    scrollbar = tk.Scrollbar(terminal_frame, command=terminal_text.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    terminal_text.config(yscrollcommand=scrollbar.set)
    
    # Configure color tags
    terminal_text.tag_configure("red", foreground="#E74C3C")
    terminal_text.tag_configure("green", foreground="#2ECC71")
    terminal_text.tag_configure("yellow", foreground="#F39C12")
    terminal_text.tag_configure("blue", foreground="#3498DB")
    terminal_text.tag_configure("white", foreground="#ECF0F1")

    current_process = None

    def save_terminal_file():
        content = terminal_text.get("1.0", "end").strip()
        with open("gui/term.txt", "w", encoding="utf-8") as f:
            f.write(content)

    # Stub functions
    def start_script():
        global current_process
        choice = script_selector.get()
        if choice and choice not in ["Choose utility...", "No scripts available"]:
            script_path = f"scripts/{choice}"
            if os.path.exists(script_path):
                if current_process and current_process.poll() is None:
                    terminal_text.config(state="normal")
                    terminal_text.insert("end", "\n>>> Another script is running. Stop it first.\n")
                    terminal_text.see("end")
                    terminal_text.config(state="disabled")
                    return
                terminal_text.config(state="normal")
                terminal_text.insert("end", f"\n>>> Starting {choice}...\n")
                terminal_text.see("end")
                terminal_text.config(state="disabled")
                def execute():
                    global current_process
                    current_process = subprocess.Popen([sys.executable, script_path], cwd=".")
                    current_process.wait()
                    current_process = None
                    root.after(0, lambda: terminal_text.config(state="normal"))
                    root.after(0, lambda: terminal_text.insert("end", f"\n>>> {choice} finished.\n"))
                    root.after(0, lambda: terminal_text.see("end"))
                    root.after(0, lambda: terminal_text.config(state="disabled"))
                threading.Thread(target=execute).start()

    def stop_script():
        global current_process
        if current_process and current_process.poll() is None:
            current_process.terminate()
            current_process.wait()
            current_process = None
            terminal_text.config(state="normal")
            terminal_text.insert("end", "\n>>> Script stopped.\n")
            terminal_text.see("end")
            terminal_text.config(state="disabled")
        else:
            terminal_text.config(state="normal")
            terminal_text.insert("end", "\n>>> No script running.\n")
            terminal_text.see("end")
            terminal_text.config(state="disabled")

    def clear_terminal():
        terminal_text.config(state="normal")
        terminal_text.delete("1.0", "end")
        terminal_text.insert("1.0", ascii_art)
        terminal_text.config(state="disabled")
        save_terminal_file()

    def write_to_terminal():
        text = write_entry.get()
        if text:
            with open("gui/term.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[COLOR:white]> User: {text}[/COLOR]\n")
        
            with open("gui/input.txt", "w", encoding="utf-8") as f:
                f.write(text)
        
            write_entry.delete(0, "end")

    def stub_source():
        terminal_text.config(state="normal")
        terminal_text.insert("end", "\n>>> Opening source...")
        terminal_text.see("end")
        terminal_text.config(state="disabled")
        # Do not save

    # Title
    title_label = ctk.CTkLabel(root, text="UTILHUB", font=("Consolas", 28, "bold"))
    title_label.grid(row=0, column=0, padx=20, pady=(15, 5))

    # Upper block
    control_panel = ctk.CTkFrame(root, corner_radius=10)
    control_panel.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    
    control_panel.grid_columnconfigure(0, weight=1)
    control_panel.grid_columnconfigure(1, weight=1)

    # Buttons block
    buttons_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
    buttons_frame.grid(row=0, column=0, padx=10, pady=15)

    # 2. START
    start_btn = ctk.CTkButton(buttons_frame, text="START", fg_color="#2ECC71", hover_color="#27AE60", text_color="black", width=120, height=40, font=("Consolas", 14, "bold"), command=start_script)
    start_btn.grid(row=0, column=0, padx=5)

    # 3. STOP
    stop_btn = ctk.CTkButton(buttons_frame, text="STOP", fg_color="#E74C3C", hover_color="#C0392B", width=120, height=40, font=("Consolas", 14, "bold"), command=stop_script)
    stop_btn.grid(row=0, column=1, padx=5)

    # 4. Script selection
    scripts_list = get_scripts_list()
    if not scripts_list:
        scripts_list = ["No scripts available"]
    script_selector = ctk.CTkOptionMenu(control_panel, values=scripts_list, width=250, height=40, font=("Consolas", 12))
    script_selector.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
    script_selector.set("Choose utility..." if scripts_list[0] != "No scripts available" else "No scripts available")

    # Lower block
    terminal_label = ctk.CTkLabel(root, text="Output stream:", font=("Consolas", 12), anchor="w")
    terminal_label.grid(row=2, column=0, padx=25, pady=(20, 0), sticky="w")
    
    # Write to terminal section
    write_frame = ctk.CTkFrame(root, fg_color="transparent")
    write_frame.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="ew")
    write_frame.grid_columnconfigure(1, weight=1)

    write_label = ctk.CTkLabel(write_frame, text="Write to Terminal:", font=("Consolas", 12))
    write_label.grid(row=0, column=0, padx=(0, 10))

    write_entry = ctk.CTkEntry(write_frame, placeholder_text="Enter text...", font=("Consolas", 12))
    write_entry.grid(row=0, column=1, sticky="ew")

    write_btn = ctk.CTkButton(write_frame, text="Send", width=80, height=30, font=("Consolas", 12), command=write_to_terminal)
    write_btn.grid(row=0, column=2, padx=(10, 0))

    # Variable to track changes (to avoid flickering)
    root.last_content = ""

    def on_closing():
        global current_process
        if current_process and current_process.poll() is None:
            current_process.terminate()
        root.destroy()
        os._exit(0)

    def load_terminal_file():
        if os.path.exists("gui/term.txt"):
            with open("gui/term.txt", "r", encoding="utf-8") as f:
                content = f.read()
            if content != root.last_content:
                terminal_text.config(state="normal")
                terminal_text.delete("1.0", "end")
                lines = content.split('\n')
                
                import re
                for line in lines:
                    color = None  
                    if line.strip():
                        parts = re.split(r'(\[COLOR:\w+\]|\[/COLOR\])', line)
                        for part in parts:
                            if not part: continue 
                            
                            if part.startswith('[COLOR:') and part.endswith(']'):
                                color = part[7:-1].lower() # Извлекаем цвет
                            elif part == '[/COLOR]':
                                color = None
                            else:
                                if color:
                                    terminal_text.insert("end", part, color)
                                else:
                                    terminal_text.insert("end", part)
                        terminal_text.insert("end", "\n")
                
                terminal_text.see("end")
                terminal_text.config(state="disabled")
                root.last_content = content
        root.after(100, load_terminal_file)

    # Bottom buttons
    bottom_frame = ctk.CTkFrame(root, fg_color="transparent")
    bottom_frame.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="ew")

    clear_btn = ctk.CTkButton(bottom_frame, text="CLEAR", fg_color="#F39C12", hover_color="#E67E22", text_color="black", width=120, height=35, font=("Consolas", 12), command=clear_terminal)
    clear_btn.grid(row=0, column=0, padx=(0, 10))

    view_source_btn = ctk.CTkButton(bottom_frame, text="Source", fg_color="transparent", border_width=2, width=150, height=35, font=("Consolas", 12), command=stub_source)
    view_source_btn.grid(row=0, column=1, sticky="e")
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    load_terminal_file()
    root.mainloop()