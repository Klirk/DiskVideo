import cv2


def play_video(file_path):
    cap = cv2.VideoCapture(file_path)

    if not cap.isOpened():
        print("Ошибка: Невозможно открыть видео файл.")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        cv2.imshow('Video', frame)

        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
