import tkinter as tk
from tkinter import messagebox
from scanner.disk_scanner import DiskScanner


class DiskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scanner")
        self.scanner = DiskScanner()

        self.scan_button = tk.Button(root, text="Сканировать диск", command=self.scan_disk)
        self.scan_button.pack(pady=10)

        self.result_text = tk.Text(root, wrap="word", width=50, height=20)
        self.result_text.pack(pady=10)

    def scan_disk(self):
        drive = self.scanner.get_last_physical_drive()
        structure = self.scanner.scan_raw_disk_structure(drive)

        if structure:
            self.result_text.insert("1.0", f"Найденная структура: {structure}")
        else:
            messagebox.showinfo("Результат", "Файлы не найдены.")
