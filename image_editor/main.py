import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk


class ImageApp:
    """Приложение для обработки изображений с базовыми функциями:
    - Загрузка изображения
    - Отображение цветовых каналов (R, G, B)
    - Изменение размера
    - Корректировка яркости
    - Рисование линий
    - Захват с камеры
    """

    def __init__(self, root):
        """Инициализация интерфейса."""
        self.root = root
        self.root.title("Image Processing App")

        self.image = None
        self.image_path = None
        self.camera_active = False
        self.cap = None

        # Основное окно с изображением
        self.image_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN, width=400, height=300)
        self.image_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.image_frame.grid_propagate(False)

        self.canvas = tk.Label(self.image_frame)
        self.canvas.pack(expand=True)

        # Кнопки
        row = 1
        tk.Button(root, text="Загрузить (Ctrl+O)", command=self.load_image).grid(row=row, column=0, pady=2)
        root.bind("<Control-o>", lambda e: self.load_image())

        row += 1
        tk.Button(root, text="Красный канал", command=lambda: self.show_channel('R')).grid(row=row, column=0, pady=2)
        tk.Button(root, text="Зеленый канал", command=lambda: self.show_channel('G')).grid(row=row, column=1, pady=2)
        tk.Button(root, text="Синий канал", command=lambda: self.show_channel('B')).grid(row=row, column=2, pady=2)

        row += 1
        tk.Label(root, text="Новый размер (ширина высота):").grid(row=row, column=0, pady=2)
        self.resize_entry = ttk.Entry(root)
        self.resize_entry.insert(0, "Например: 800 600")
        self.resize_entry.bind("<FocusIn>", lambda e: self.resize_entry.delete(0, tk.END))
        self.resize_entry.grid(row=row, column=1, pady=2)
        tk.Button(root, text="Изменить размер", command=self.resize_image).grid(row=row, column=2, pady=2)

        row += 1
        tk.Label(root, text="Яркость (-255..255):").grid(row=row, column=0, pady=2)
        self.brightness_entry = ttk.Entry(root)
        self.brightness_entry.grid(row=row, column=1, pady=2)
        tk.Button(root, text="Применить", command=self.adjust_brightness).grid(row=row, column=2, pady=2)

        row += 1
        tk.Label(root, text="Линия (x1 y1 x2 y2 толщина):").grid(row=row, column=0, pady=2)
        self.line_entry = ttk.Entry(root)
        self.line_entry.grid(row=row, column=1, pady=2)
        tk.Button(root, text="Нарисовать", command=self.draw_line).grid(row=row, column=2, pady=2)

        row += 1
        tk.Button(
            root,
            text="Сделать фото с камеры",
            command=self.capture_from_camera
        ).grid(row=row, column=0, pady=2)

        row += 1
        tk.Button(root, text="Сбросить изменения", command=self.reset_image).grid(row=row, column=0, pady=2)

    def load_image(self):
        """Загружает изображение из файла."""
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if not path:
            return
        try:
            img = cv2.imread(path)
            if img is None:
                raise ValueError("Не удалось загрузить изображение.")
            self.image_path = path
            self.image = img
            self.show_image(img)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка загрузки: {str(e)}")

    def show_image(self, img):
        """Отображает изображение с сохранением пропорций."""
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)

        # Масштабирование с сохранением пропорций
        max_width, max_height = 400, 300
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        new_size = (int(width * ratio), int(height * ratio))
        image = image.resize(new_size, Image.LANCZOS)

        photo = ImageTk.PhotoImage(image=image)
        self.canvas.configure(image=photo)
        self.canvas.image = photo

    def capture_from_camera(self):
        """Делает снимок с камеры и сохраняет его как загруженное изображение."""
        cap = cv2.VideoCapture(0)  # Открываем камеру

        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к камере.")
            return

        ret, frame = cap.read()  # Делаем снимок
        cap.release()  # Закрываем камеру

        if not ret:
            messagebox.showerror("Ошибка", "Не удалось получить кадр с камеры.")
            return

        self.image = frame
        self.image_path = "camera_capture.jpg"  # Можно сохранить в файл, если нужно
        self.show_image(frame)

    def start_camera_stream(self):
        """Запускает потоковое видео с камеры."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к камере.")
            return
        self.camera_active = True
        self.update_camera_frame()


    def stop_camera_stream(self):
        """Останавливает потоковое видео."""
        if self.cap:
            self.cap.release()
        self.camera_active = False

    def show_channel(self, channel):
        """Отображает выбранный цветовой канал (R, G, B)."""
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return

        ch_idx = {'B': 0, 'G': 1, 'R': 2}.get(channel)
        if ch_idx is None:
            return

        channel_img = self.image.copy()
        channel_img[:, :, [i for i in range(3) if i != ch_idx]] = 0
        self.show_image(channel_img)

    def resize_image(self):
        """Изменяет размер изображения."""
        if self.image is None:
            return

        try:
            width, height = map(int, self.resize_entry.get().split())
            if width <= 0 or height <= 0:
                raise ValueError("Размеры должны быть положительными.")
            resized = cv2.resize(self.image, (width, height))
            self.image = resized
            self.show_image(resized)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {str(e)}")

    def adjust_brightness(self):
        """Увеличивает яркость изображения на заданное значение."""
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return

        try:
            value = int(self.brightness_entry.get())

            # Увеличиваем яркость (значение добавляется к каждому каналу)
            bright_image = cv2.add(self.image, value)

            self.image = bright_image
            self.show_image(bright_image)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число для яркости.")

    def draw_line(self):
        """Рисует линию на изображении."""
        if self.image is None:
            return

        try:
            x1, y1, x2, y2, thickness = map(int, self.line_entry.get().split())
            img_copy = self.image.copy()
            cv2.line(img_copy, (x1, y1), (x2, y2), (0, 255, 0), thickness)
            self.image = img_copy
            self.show_image(img_copy)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Некорректный ввод: {str(e)}")

    def reset_image(self):
        """Сбрасывает изображение к оригиналу."""
        if self.image_path:
            self.image = cv2.imread(self.image_path)
            self.show_image(self.image)
        elif hasattr(self, 'original_image'):
            self.image = self.original_image.copy()
            self.show_image(self.image)
        else:
            messagebox.showwarning("Внимание", "Нет изображения для сброса.")


def main():
    """Функция для запуска из точки входа."""
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()