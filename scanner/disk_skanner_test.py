import re
import win32file

def scan_partition_for_video(drive, partition_offset, partition_size, buffer_size=4096):
    structure = {}
    try:
        # Открываем диск в режиме сырого доступа
        handle = win32file.CreateFile(
            drive,
            win32file.GENERIC_READ,
            win32file.FILE_SHARE_READ | win32file.FILE_SHARE_WRITE,
            None,
            win32file.OPEN_EXISTING,
            0,
            None
        )

        # Сдвигаем указатель на начало нужного раздела
        win32file.SetFilePointer(handle, partition_offset, win32file.FILE_BEGIN)

        offset = 0
        max_offset = partition_size

        while offset < max_offset:
            # Чтение данных из текущего раздела
            data = win32file.ReadFile(handle, buffer_size)[1]

            # Поиск имен видеофайлов (на основе вашего паттерна)
            video_files = re.findall(rb'\d{2}\.\d{2}\.\d{2}-\d{2}\.\d{2}\.\d{2}\[R\]\[\@\d+\]\[\d+\]\.h264', data)

            for file in video_files:
                file_name = file.decode('utf-8')
                if file_name not in structure:
                    structure[file_name] = offset + partition_offset

            # Обновление смещения
            offset += buffer_size

        win32file.CloseHandle(handle)
    except Exception as e:
        print(f"Ошибка при сканировании раздела {drive}: {e}")

    return structure

# Указываем путь к физическому диску и параметры раздела
drive = r"\\.\PhysicalDrive2"  # Замените на правильный номер диска
partition_offset = 618496  # Оффсет начала раздела
partition_size = 624521216  # Размер раздела

# Запуск функции сканирования
result = scan_partition_for_video(drive, partition_offset, partition_size)

# Вывод результатов
if result:
    print("Найдены видеофайлы:")
    for file_name, position in result.items():
        print(f"Файл: {file_name}, смещение: {position}")
else:
    print("Видео файлы не найдены.")
