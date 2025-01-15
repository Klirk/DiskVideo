import subprocess

import win32file
import re

class DiskScanner:
    def get_last_physical_drive(self):
        """Получает список дисков, подключенных через USB, с помощью PowerShell."""
        try:
            command = (
                'powershell "Get-Disk | '
                'Where-Object { $_.BusType -eq \'USB\' } | '
                'Select-Object -Property Number,FriendlyName,Size | Format-Table -AutoSize"'
            )
            result = subprocess.run(command, capture_output=True, text=True, shell=True)

            usb_disks = []
            for line in result.stdout.splitlines()[2:]:  # Пропускаем заголовки таблицы
                parts = line.strip().split()
                if len(parts) >= 3:
                    disk_number = parts[0]
                    friendly_name = " ".join(parts[1:-1])
                    size = parts[-1]
                    usb_disks.append((disk_number, friendly_name, size))
        except Exception as e:
            print(f"Ошибка при выполнении команды: {e}")
            return []

        if not usb_disks:
            print("USB-диски не найдены.")
            return

        print("Найденные USB-диски:")
        for disk in usb_disks:
            print(f"Номер: {disk[0]}, Имя: {disk[1]}, Размер: {disk[2]}")

        disk_number = usb_disks[1][0]  # Выбираем первый USB-диск
        drive_path = f"\\\\.\\PhysicalDrive{disk_number}" # Укажите актуальный диск
        return drive_path

    def scan_raw_disk_structure(self, drive):
        import win32file
        import re

        structure = {}
        try:
            handle = win32file.CreateFile(
                drive, win32file.GENERIC_READ, win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
                None, win32file.OPEN_EXISTING, 0, None
            )
            buffer_size = 4096  # Размер буфера чтения
            current_directory = "idea0"
            structure[current_directory] = {}

            # Указатель чтения данных
            offset = 0

            while True:
                # Чтение данных с позиции offset
                win32file.SetFilePointer(handle, offset, win32file.FILE_BEGIN)
                data = win32file.ReadFile(handle, buffer_size)[1]

                if not data or len(data) < buffer_size:  # Проверка на конец файла
                    break

                date_match = re.search(rb'\d{4}-\d{2}-\d{2}', data)
                file_match = re.findall(rb'\d{2}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}\[R\]\[\@\d+\]\[\d+\]\.h264', data)

                if date_match:
                    date_folder = date_match.group().decode('utf-8')
                    if date_folder not in structure[current_directory]:
                        structure[current_directory][date_folder] = {}

                if date_match:
                    for file in file_match:
                        file_name = file.decode('utf-8')
                        structure[current_directory][date_folder][file_name] = "h264"

                # Увеличиваем offset для чтения следующего блока данных
                offset += buffer_size

            win32file.CloseHandle(handle)
        except Exception as e:
            print(f"Ошибка при сканировании {drive}: {e}")

        return structure