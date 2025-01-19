import subprocess
import win32file
import re
import os

class DiskScanner:
    def get_last_physical_drive(self):
        """Получить последний подключенный USB-диск."""
        try:
            command = (
                'powershell "Get-Disk | '
                'Where-Object { $_.BusType -eq \'USB\' } | '
                'Sort-Object -Property Number -Descending | '
                'Select-Object -First 1 -ExpandProperty Number"'
            )
            result = subprocess.run(command, capture_output=True, text=True, shell=True)
            disk_number = result.stdout.strip()

            if not disk_number:
                print("USB-диски не найдены.")
                return None

            return f"\\\\.\\PhysicalDrive{disk_number}"
        except Exception as e:
            print(f"Ошибка при определении последнего USB-диска: {e}")
            return None

    def scan_raw_disk_structure(self, drive, buffer_size=4096):
        """Сканирование диска на предмет структуры каталогов."""
        structure = {}
        try:
            handle = win32file.CreateFile(
                drive,
                win32file.GENERIC_READ,
                win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
                None,
                win32file.OPEN_EXISTING,
                0,
                None,
            )

            offset = 0
            max_iterations = 10 ** 6
            iterations = 0

            while True:
                iterations += 1
                if iterations > max_iterations:
                    print("Превышено максимальное количество итераций.")
                    break

                win32file.SetFilePointer(handle, offset, win32file.FILE_BEGIN)
                data = win32file.ReadFile(handle, buffer_size)[0]

                if not data or len(data) < buffer_size:
                    break

                # Пример паттернов для поиска:
                catalog_match = re.search(rb'catalog_name/', data)  # Пример каталога
                date_match = re.search(rb'\d{2}-\d{2}-\d{4}', data)  # Пример даты
                file_match = re.findall(rb'\d{2}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}\[R\]\[\@\d+\]\[\d+\]\.h264', data)  # Пример файлов

                if catalog_match and date_match:
                    # Извлекаем дату каталога
                    date_folder = date_match.group().decode('utf-8')

                    if date_folder not in structure:
                        structure[date_folder] = []

                    # Добавляем найденные файлы в структуру
                    for file in file_match:
                        file_name = file.decode('utf-8')
                        structure[date_folder].append(file_name)

                offset += buffer_size

            win32file.CloseHandle(handle)
        except Exception as e:
            print(f"Ошибка при сканировании {drive}: {e}")

        return structure

# Пример использования:
scanner = DiskScanner()
last_drive = scanner.get_last_physical_drive()
if last_drive:
    structure = scanner.scan_raw_disk_structure(last_drive)
    if structure:
        print("Структура данных:", structure)
    else:
        print("Структура данных не найдена.")
