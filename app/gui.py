import tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox

import os

from modules.rva_updater import parse_dump_file, update_main_cpp
from modules.apk_injector import inject_assets
from modules.smali_injector import inject_oncreate
from modules.manifest_editor import modify_manifest
from modules.activity_detector import get_launcher_activity, activity_to_smali_path
from modules.git_backup import backup_to_git


class ModdingSuiteApp:

    def __init__(self):

        self.root = tk.Tk()
        self.root.title("Modding Automation Suite")
        self.root.geometry("920x640")
        self.root.resizable(False, False)

        # RVA
        self.dump_path = ""
        self.main_path = ""

        # APK
        self.apk_folder = ""
        self.app_debug_folder = ""

        # Backup
        self.backup_files = []
        self.repo_folder = ""

        self.create_ui()

    # =====================================================
    # UI CREATION
    # =====================================================

    def create_ui(self):

        style = ttk.Style()
        style.theme_use("clam")

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.rva_tab = ttk.Frame(notebook)
        self.apk_tab = ttk.Frame(notebook)
        self.backup_tab = ttk.Frame(notebook)
        self.settings_tab = ttk.Frame(notebook)

        notebook.add(self.rva_tab, text="RVA Updater")
        notebook.add(self.apk_tab, text="APK Injector")
        notebook.add(self.backup_tab, text="Backup")
        notebook.add(self.settings_tab, text="Settings")

        self.build_rva_tab()
        self.build_apk_tab()
        self.build_backup_tab()
        self.build_settings_tab()

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")

        status_bar = ttk.Label(
            self.root,
            textvariable=self.status_var,
            relief="sunken",
            anchor="w",
            padding=5
        )
        status_bar.pack(fill="x", side="bottom")

    # =====================================================
    # RVA TAB
    # =====================================================

    def build_rva_tab(self):

        container = ttk.LabelFrame(
            self.rva_tab,
            text="RVA Auto Updater",
            padding=20
        )
        container.pack(fill="x", padx=20, pady=20)

        ttk.Button(
            container,
            text="Select dump.cs",
            command=self.select_dump,
            width=30
        ).pack(pady=5)

        ttk.Button(
            container,
            text="Select main.cpp",
            command=self.select_main,
            width=30
        ).pack(pady=5)

        ttk.Button(
            container,
            text="Update RVAs",
            command=self.run_rva_update,
            width=30
        ).pack(pady=15)

    def select_dump(self):

        path = filedialog.askopenfilename(
            title="Select dump.cs",
            filetypes=[("C# Dump", "*.cs"), ("All Files", "*.*")]
        )

        if path:
            self.dump_path = path
            self.status_var.set("dump.cs selected")

    def select_main(self):

        path = filedialog.askopenfilename(
            title="Select main.cpp",
            filetypes=[("C++ File", "*.cpp"), ("All Files", "*.*")]
        )

        if path:
            self.main_path = path
            self.status_var.set("main.cpp selected")

    def run_rva_update(self):

        if not self.dump_path or not self.main_path:
            messagebox.showerror("Error", "Select dump.cs and main.cpp first")
            return

        try:

            self.status_var.set("Parsing dump.cs...")
            rva_map = parse_dump_file(self.dump_path)

            self.status_var.set("Updating RVAs...")
            updated, missing = update_main_cpp(
                self.main_path,
                rva_map
            )

            messagebox.showinfo(
                "Done",
                f"Updated: {updated}\nMissing: {missing}"
            )

            self.status_var.set("RVA update complete")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =====================================================
    # APK TAB
    # =====================================================

    def build_apk_tab(self):

        container = ttk.LabelFrame(
            self.apk_tab,
            text="APK Injection",
            padding=20
        )
        container.pack(fill="x", padx=20, pady=20)

        ttk.Button(
            container,
            text="Select Decompiled APK Folder",
            command=self.select_apk_folder,
            width=40
        ).pack(pady=5)

        ttk.Button(
            container,
            text="Select app-debug Folder",
            command=self.select_app_debug,
            width=40
        ).pack(pady=5)

        ttk.Button(
            container,
            text="Inject Mod Menu",
            command=self.run_injector,
            width=40
        ).pack(pady=15)

    def select_apk_folder(self):

        path = filedialog.askdirectory(
            title="Select Decompiled APK Folder"
        )

        if path:
            self.apk_folder = path
            self.status_var.set("APK folder selected")

    def select_app_debug(self):

        path = filedialog.askdirectory(
            title="Select app-debug Folder"
        )

        if path:
            self.app_debug_folder = path
            self.status_var.set("app-debug folder selected")

    def run_injector(self):

        if not self.apk_folder or not self.app_debug_folder:
            messagebox.showerror(
                "Error",
                "Select APK folder and app-debug folder first"
            )
            return

        try:

            self.status_var.set("Copying mod menu files...")

            inject_assets(
                self.apk_folder,
                self.app_debug_folder
            )

            self.status_var.set("Detecting launcher activity...")

            launcher = get_launcher_activity(self.apk_folder)

            smali_path = activity_to_smali_path(
                self.apk_folder,
                launcher
            )

            self.status_var.set(f"Launcher Activity: {launcher}")

            inject_oncreate(smali_path)

            self.status_var.set("Modifying AndroidManifest...")

            modify_manifest(self.apk_folder)

            messagebox.showinfo(
                "Success",
                "Mod menu injected successfully!"
            )

            self.status_var.set("Injection complete")

        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.status_var.set("Injection failed")

    # =====================================================
    # BACKUP TAB
    # =====================================================

    def build_backup_tab(self):

        container = ttk.LabelFrame(
            self.backup_tab,
            text="Git Backup",
            padding=20
        )
        container.pack(fill="x", padx=20, pady=20)

        ttk.Button(
            container,
            text="Select Files",
            command=self.select_backup_files,
            width=30
        ).pack(pady=5)

        ttk.Button(
            container,
            text="Select Repo Folder",
            command=self.select_repo_folder,
            width=30
        ).pack(pady=5)

        ttk.Button(
            container,
            text="Upload Backup",
            command=self.run_backup,
            width=30
        ).pack(pady=15)

    def select_backup_files(self):

        paths = filedialog.askopenfilenames(
            title="Select Files to Backup"
        )

        if paths:
            self.backup_files = list(paths)
            self.status_var.set(f"{len(paths)} files selected")

    def select_repo_folder(self):

        path = filedialog.askdirectory(
            title="Select Cloned Git Repository Folder"
        )

        if path:
            self.repo_folder = path
            self.status_var.set("Repo folder selected")

    def run_backup(self):

        if not self.backup_files or not self.repo_folder:
            messagebox.showerror(
                "Error",
                "Select files and repo folder first"
            )
            return

        try:

            result = backup_to_git(
                self.backup_files,
                self.repo_folder
            )

            if result["status"] == "No changes":

                messagebox.showinfo(
                    "Info",
                    "No changes detected."
                )

            else:

                messagebox.showinfo(
                    "Success",
                    f"Backup successful!\n\n{result['message']}"
                )

            self.status_var.set("Backup complete")

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # =====================================================
    # SETTINGS TAB
    # =====================================================

    def build_settings_tab(self):

        container = ttk.LabelFrame(
            self.settings_tab,
            text="Settings",
            padding=20
        )
        container.pack(fill="x", padx=20, pady=20)

        ttk.Label(
            container,
            text="More features coming soon...",
            font=("Arial", 11)
        ).pack(pady=10)

    # =====================================================

    def run(self):
        self.root.mainloop()