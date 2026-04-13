# UtilHub - Central Utility Dashboard
# Copyright (C) 2026 den89023
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License.

import customtkinter as ctk
import tkinter as tk
import os
import subprocess
import threading
import sys
from pygments.lexers import PythonLexer

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from core.file_manager import get_scripts_list

current_process = None

def start_app():
    global current_process

    root = ctk.CTk()
    root.title("UtilHub v0.4")
    root.geometry("900x650")
    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(3, weight=1)

    # ── Views ──────────────────────────────────────────────────────────────────
    main_view = ctk.CTkFrame(root, fg_color="transparent")
    main_view.pack(expand=True, fill="both")
    main_view.grid_columnconfigure(0, weight=1)
    main_view.grid_rowconfigure(4, weight=1)

    editor_view = ctk.CTkFrame(root, fg_color="transparent")

    ascii_art = (
        "╔══════════════════════════════════════════╗\n"
        "║                UTILHUB                   ║\n"
        "╟──────────────────────────────────────────╢\n"
        "║  Author: den89023                        ║\n"
        "║  Year: 2026                              ║\n"
        "║  License: GNU GPL v3 (since 2007)        ║\n"
        "╚══════════════════════════════════════════╝\n\n"
    )

    # ── Editor top bar ─────────────────────────────────────────────────────────
    top_bar = ctk.CTkFrame(editor_view, height=45, corner_radius=0)
    top_bar.pack(fill="x", padx=0, pady=0)

    editor_title_var = tk.StringVar(value="")
    editor_title_label = ctk.CTkLabel(
        top_bar, textvariable=editor_title_var,
        font=("Consolas", 13, "bold")
    )
    editor_title_label.pack(side="left", padx=(12, 0))

    # ── Three-dot dropdown menu ────────────────────────────────────────────────
    menu_popup = None

    def close_menu():
        nonlocal menu_popup
        if menu_popup and menu_popup.winfo_exists():
            menu_popup.destroy()
        menu_popup = None

    def open_three_dot_menu():
        nonlocal menu_popup
        if menu_popup and menu_popup.winfo_exists():
            close_menu()
            return

        popup = tk.Toplevel(root)
        popup.overrideredirect(True)
        popup.configure(bg="#2B2B2B")

        btn_x = three_dot_btn.winfo_rootx()
        btn_y = three_dot_btn.winfo_rooty() + three_dot_btn.winfo_height() + 2
        popup.geometry(f"220x120+{btn_x - 160}+{btn_y}")
        menu_popup = popup

        def menu_item(text, command, color="#FFFFFF"):
            b = tk.Button(
                popup, text=text, font=("Consolas", 12),
                bg="#2B2B2B", fg=color,
                activebackground="#3A3A3A", activeforeground=color,
                relief="flat", anchor="w", padx=14, pady=7,
                cursor="hand2",
                command=lambda: [close_menu(), command()]
            )
            b.pack(fill="x")

        menu_item("💾  Save",               do_save)
        menu_item("✔  Save & Exit",         do_save_and_exit, color="#2ECC71")
        menu_item("✖  Exit without saving", do_exit_no_save,  color="#E74C3C")

        popup.bind("<FocusOut>", lambda e: close_menu())
        popup.focus_set()

    three_dot_btn = ctk.CTkButton(
        top_bar, text="• • •", width=60, height=32,
        font=("Consolas", 14, "bold"),
        fg_color="transparent", hover_color="#3A3A3A",
        command=open_three_dot_menu
    )
    three_dot_btn.pack(side="right", padx=10, pady=6)

    # ── Editor text area ───────────────────────────────────────────────────────
    editor_text = ctk.CTkTextbox(editor_view, font=("Consolas", 14))
    editor_text.pack(expand=True, fill="both", padx=10, pady=(4, 10))

    # ── Syntax highlighting ────────────────────────────────────────────────────
    def highlight(txt_widget):
        content = txt_widget.get("1.0", "end-1c")
        for tag in txt_widget.tag_names():
            txt_widget.tag_remove(tag, "1.0", "end")
        lexer = PythonLexer()
        index = "1.0"
        for token_type, value in lexer.get_tokens(content):
            tag_name = str(token_type)
            end_index = txt_widget.index(f"{index} + {len(value)} chars")
            if "Keyword" in tag_name:
                txt_widget.tag_config(tag_name, foreground="#C678DD")
            elif "Name.Function" in tag_name or "Name.Method" in tag_name:
                txt_widget.tag_config(tag_name, foreground="#61AFEF")
            elif "Literal.String" in tag_name:
                txt_widget.tag_config(tag_name, foreground="#98C379")
            elif "Comment" in tag_name:
                txt_widget.tag_config(tag_name, foreground="#5C6370")
            elif "Name.Builtin" in tag_name:
                txt_widget.tag_config(tag_name, foreground="#D19A66")
            elif "Operator" in tag_name or "Punctuation" in tag_name:
                txt_widget.tag_config(tag_name, foreground="#56B6C2")
            txt_widget.tag_add(tag_name, index, end_index)
            index = end_index

    # ── Editor actions (used by menu) ──────────────────────────────────────────
    def do_save():
        name = script_selector.get()
        if name not in ("Choose utility...", "No scripts available"):
            with open(f"scripts/{name}", "w", encoding="utf-8") as f:
                f.write(editor_text.get("1.0", "end-1c"))

    def do_save_and_exit():
        do_save()
        editor_view.pack_forget()
        main_view.pack(expand=True, fill="both")

    def do_exit_no_save():
        editor_view.pack_forget()
        main_view.pack(expand=True, fill="both")

    def open_editor():
        selected = script_selector.get()
        if selected in ("Choose utility...", "No scripts available"):
            return
        editor_title_var.set(selected)
        script_path = f"scripts/{selected}"
        if os.path.exists(script_path):
            try:
                with open(script_path, "r", encoding="utf-8") as f:
                    content = f.read()
                editor_text.delete("1.0", "end")
                editor_text.insert("1.0", content)
                highlight(editor_text)
            except Exception as e:
                print(f"Error reading file: {e}")
        main_view.pack_forget()
        editor_view.pack(expand=True, fill="both")

    # ── Terminal ───────────────────────────────────────────────────────────────
    terminal_frame = ctk.CTkFrame(main_view, corner_radius=10)
    terminal_frame.grid(row=4, column=0, padx=20, pady=(5, 15), sticky="nsew")
    terminal_frame.grid_columnconfigure(0, weight=1)
    terminal_frame.grid_rowconfigure(0, weight=1)

    terminal_text = tk.Text(
        terminal_frame, width=80, height=15, font=("Consolas", 12),
        bg="#1E1E1E", fg="#F1C40F", insertbackground="#F1C40F",
        wrap=tk.WORD, state="disabled"
    )
    terminal_text.grid(row=0, column=0, sticky="nsew")

    scrollbar = tk.Scrollbar(terminal_frame, command=terminal_text.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    terminal_text.config(yscrollcommand=scrollbar.set)

    terminal_text.tag_configure("red",    foreground="#E74C3C")
    terminal_text.tag_configure("green",  foreground="#2ECC71")
    terminal_text.tag_configure("yellow", foreground="#F39C12")
    terminal_text.tag_configure("blue",   foreground="#3498DB")
    terminal_text.tag_configure("white",  foreground="#ECF0F1")

    # ── Script controls ────────────────────────────────────────────────────────
    def start_script():
        global current_process
        choice = script_selector.get()
        if choice in ("Choose utility...", "No scripts available"):
            return
        script_path = f"scripts/{choice}"
        if not os.path.exists(script_path):
            return
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

        threading.Thread(target=execute, daemon=True).start()

    def stop_script():
        global current_process
        terminal_text.config(state="normal")
        if current_process and current_process.poll() is None:
            current_process.terminate()
            current_process.wait()
            current_process = None
            terminal_text.insert("end", "\n>>> Script stopped.\n")
        else:
            terminal_text.insert("end", "\n>>> No script running.\n")
        terminal_text.see("end")
        terminal_text.config(state="disabled")

    def save_terminal_file():
        content = terminal_text.get("1.0", "end").strip()
        os.makedirs("gui", exist_ok=True)
        with open("gui/term.txt", "w", encoding="utf-8") as f:
            f.write(content)

    def clear_terminal():
        terminal_text.config(state="normal")
        terminal_text.delete("1.0", "end")
        terminal_text.insert("1.0", ascii_art)
        terminal_text.config(state="disabled")
        save_terminal_file()

    def write_to_terminal():
        text = write_entry.get()
        if text:
            os.makedirs("gui", exist_ok=True)
            with open("gui/term.txt", "a", encoding="utf-8") as f:
                f.write(f"\n[COLOR:white]> User: {text}[/COLOR]\n")
            with open("gui/input.txt", "w", encoding="utf-8") as f:
                f.write(text)
            write_entry.delete(0, "end")

    # ── Main view widgets ──────────────────────────────────────────────────────
    title_label = ctk.CTkLabel(main_view, text="UTILHUB", font=("Consolas", 28, "bold"))
    title_label.grid(row=0, column=0, padx=20, pady=(15, 5))

    control_panel = ctk.CTkFrame(main_view, corner_radius=10)
    control_panel.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
    control_panel.grid_columnconfigure(0, weight=1)
    control_panel.grid_columnconfigure(1, weight=1)

    buttons_frame = ctk.CTkFrame(control_panel, fg_color="transparent")
    buttons_frame.grid(row=0, column=0, padx=10, pady=10, sticky="w")

    start_btn = ctk.CTkButton(
        buttons_frame, text="START",
        fg_color="#2ECC71", hover_color="#27AE60",
        width=120, height=40, font=("Consolas", 14, "bold"),
        command=start_script
    )
    start_btn.grid(row=0, column=0, padx=5)

    stop_btn = ctk.CTkButton(
        buttons_frame, text="STOP",
        fg_color="#E74C3C", hover_color="#C0392B",
        width=120, height=40, font=("Consolas", 14, "bold"),
        command=stop_script
    )
    stop_btn.grid(row=0, column=1, padx=5)

    scripts_list = get_scripts_list() or ["No scripts available"]
    script_selector = ctk.CTkOptionMenu(
        control_panel, values=scripts_list,
        width=250, height=40, font=("Consolas", 12)
    )
    script_selector.grid(row=0, column=1, padx=10, pady=15, sticky="ew")
    script_selector.set(
        "Choose utility..." if scripts_list[0] != "No scripts available"
        else "No scripts available"
    )

    terminal_label = ctk.CTkLabel(main_view, text="Output stream:", font=("Consolas", 12), anchor="w")
    terminal_label.grid(row=2, column=0, padx=25, pady=(20, 0), sticky="w")

    write_frame = ctk.CTkFrame(main_view, fg_color="transparent")
    write_frame.grid(row=3, column=0, padx=20, pady=(5, 0), sticky="ew")
    write_frame.grid_columnconfigure(1, weight=1)

    write_label = ctk.CTkLabel(write_frame, text="Write to Terminal:", font=("Consolas", 12))
    write_label.grid(row=0, column=0, padx=(0, 10))

    write_entry = ctk.CTkEntry(write_frame, placeholder_text="Enter text...", font=("Consolas", 12))
    write_entry.grid(row=0, column=1, sticky="ew")

    write_btn = ctk.CTkButton(
        write_frame, text="Send",
        width=80, height=30, font=("Consolas", 12),
        command=write_to_terminal
    )
    write_btn.grid(row=0, column=2, padx=(10, 0))

    bottom_frame = ctk.CTkFrame(main_view, fg_color="transparent")
    bottom_frame.grid(row=5, column=0, padx=20, pady=(0, 15), sticky="ew")

    clear_btn = ctk.CTkButton(
        bottom_frame, text="CLEAR",
        fg_color="#F39C12", hover_color="#E67E22",
        text_color="black", width=120, height=35, font=("Consolas", 12),
        command=clear_terminal
    )
    clear_btn.grid(row=0, column=0, padx=(0, 10))

    view_source_btn = ctk.CTkButton(
        bottom_frame, text="Source",
        fg_color="transparent", border_width=2,
        width=150, height=35, font=("Consolas", 12),
        command=open_editor
    )
    view_source_btn.grid(row=0, column=1, sticky="e")

    # ── Terminal file loader ───────────────────────────────────────────────────
    root.last_content = ""

    def load_terminal_file():
        if os.path.exists("gui/term.txt"):
            with open("gui/term.txt", "r", encoding="utf-8") as f:
                content = f.read()
            if content != root.last_content:
                import re
                terminal_text.config(state="normal")
                terminal_text.delete("1.0", "end")
                for line in content.split('\n'):
                    if line.strip():
                        color = None
                        for part in re.split(r'(\[COLOR:\w+\]|\[/COLOR\])', line):
                            if not part:
                                continue
                            if part.startswith('[COLOR:') and part.endswith(']'):
                                color = part[7:-1].lower()
                            elif part == '[/COLOR]':
                                color = None
                            else:
                                terminal_text.insert("end", part, color if color else "")
                    terminal_text.insert("end", "\n")
                terminal_text.see("end")
                terminal_text.config(state="disabled")
                root.last_content = content
        root.after(100, load_terminal_file)

    # ── Shutdown ───────────────────────────────────────────────────────────────
    def on_closing():
        global current_process
        if current_process and current_process.poll() is None:
            current_process.terminate()
        root.destroy()
        os._exit(0)

    root.protocol("WM_DELETE_WINDOW", on_closing)
    load_terminal_file()
    root.mainloop()