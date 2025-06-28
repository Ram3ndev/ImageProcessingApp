

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import cv2
import numpy as np
from PIL import Image, ImageTk

class ImageApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        self.image = None
        self.image_path = None

        self.image_frame = tk.Frame(root, bd=2, relief=tk.SUNKEN, width=400, height=300)
        self.image_frame.grid(row=0, column=0, columnspan=3, padx=10, pady=10)
        self.image_frame.grid_propagate(False)

        self.canvas = tk.Label(self.image_frame)
        self.canvas.pack(expand=True)

        row = 1
        tk.Button(root, text="Загрузить изображение", command=self.load_image).grid(row=row, column=0, pady=2)

        row+=1

        tk.Button(root, text="Показать красный канал изображения", command=lambda: self.show_channel('R')).grid(row=row, column=0, pady=2)
        tk.Button(root, text="Показать зеленый канал изображения", command=lambda: self.show_channel('G')).grid(row=row, column=1, pady=2)
        tk.Button(root, text="Показать синий канал изображения", command=lambda: self.show_channel('B')).grid(row=row, column=2, pady=2)

        row += 1
        tk.Label(root, text="Новый размер (ширина высота):").grid(row=row, column=0, pady=2)
        self.resize_entry = tk.Entry(root)
        self.resize_entry.grid(row=row, column=1, pady=2)
        tk.Button(root, text="Изменить размер", command=self.resize_image).grid(row=row, column=2, pady=2)

        row += 1
        tk.Label(root, text="Яркость (+число):").grid(row=row, column=0, pady=2)
        self.brightness_entry = tk.Entry(root)
        self.brightness_entry.grid(row=row, column=1, pady=2)
        tk.Button(root, text="Повысить яркость", command=self.increase_brightness).grid(row=row, column=2, pady=2)

        row += 1
        tk.Label(root, text="Линия (x1 y1 x2 y2 толщина):").grid(row=row, column=0, pady=2)
        self.line_entry = tk.Entry(root)
        self.line_entry.grid(row=row, column=1, pady=2)
        tk.Button(root, text="Нарисовать линию", command=self.draw_line).grid(row=row, column=2, pady=2)

        tk.Button(root, text="Сделать снимок с камеры", command=self.capture_from_camera).grid(row=row, column=0,
                                                                                               pady=2)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
        if path:
            self.image_path = path
            img = cv2.imread(path)
            if img is None:
                messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
                return
            self.image = img
            self.show_image(img)

    def show_image(self, img):
        rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(rgb)
        image.thumbnail((400, 300))  # Ограничение по размеру в рамке
        photo = ImageTk.PhotoImage(image=image)
        self.canvas.configure(image=photo)
        self.canvas.image = photo

    def capture_from_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к камере.")
            return
        ret, frame = cap.read()
        cap.release()
        if not ret:
            messagebox.showerror("Ошибка", "Не удалось получить кадр с камеры.")
            return
        self.image = frame
        self.show_image(frame)

    def show_channel(self, channel):
        if self.image is None:
            messagebox.showwarning("Внимание", "Сначала загрузите изображение.")
            return
        if channel not in ('R', 'G', 'B'):
            messagebox.showerror("Ошибка", "Неверный канал.")
            return
        ch_idx = {'B': 0, 'G': 1, 'R': 2}[channel]
        channel_img = self.image[:, :, ch_idx]
        zero = np.zeros_like(channel_img)
        if channel == 'R':
            colored_img = cv2.merge([zero, zero, channel_img])  # B, G, R
        elif channel == 'G':
            colored_img = cv2.merge([zero, channel_img, zero])
        else:  # 'B'
            colored_img = cv2.merge([channel_img, zero, zero])
        self.show_image(colored_img)

    def resize_image(self):
        if self.image is None:
            return
        try:
            width, height = map(int, self.resize_entry.get().split())
            resized = cv2.resize(self.image, (width, height))
            self.image = resized
            self.show_image(resized)
        except:
            messagebox.showerror("Ошибка", "Введите два числа через пробел (ширина высота).")

    def increase_brightness(self):
        if self.image is None:
            return
        try:
            value = int(self.brightness_entry.get())
            bright = cv2.convertScaleAbs(self.image, alpha=1, beta=value)
            self.image = bright
            self.show_image(bright)
        except:
            messagebox.showerror("Ошибка", "Введите целое число для яркости.")

    def draw_line(self):
        if self.image is None:
            return
        try:
            x1, y1, x2, y2, thickness = map(int, self.line_entry.get().split())
            img_copy = self.image.copy()
            cv2.line(img_copy, (x1, y1), (x2, y2), (0, 255, 0), thickness)
            self.image = img_copy
            self.show_image(img_copy)
        except:
            messagebox.showerror("Ошибка", "Введите координаты и толщину через пробел (x1 y1 x2 y2 толщина).")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageApp(root)
    root.mainloop()
