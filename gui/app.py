import tkinter as tk
from tkinter import messagebox
from scanner.disk_scanner import DiskScanner


class DiskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Disk Scanner")
        self.scanner = DiskScanner()

        self.scan_button = tk.Button(root, text="Сканировать последний диск", command=self.scan_last_disk)
        self.scan_button.pack(pady=10)

        self.result_text = tk.Text(root, wrap="word", width=70, height=20)
        self.result_text.pack(pady=10)

    def scan_last_disk(self):
        self.result_text.delete("1.0", tk.END)

        drive = self.scanner.get_last_physical_drive()
        if not drive:
            messagebox.showinfo("Результат", "Последний USB-диск не найден.")
            return

        self.result_text.insert("1.0", f"Сканируем диск: {drive}...\n")
        structure = self.scanner.scan_raw_disk_structure(drive)

        if structure:
            self.result_text.insert("end", f"Найденная структура:\n{structure}\n")
        else:
            self.result_text.insert("end", "Файлы не найдены.")
