# 🖼️ Visual Processing App - Обработка изображений с веб-камерой

*Простое приложение для обработки изображений и работы с веб-камерой*

## 🗒️ Описание
Visual Processing App - это кроссплатформенное приложение с графическим интерфейсом на Tkinter для базовой обработки изображений и захвата фото с веб-камеры.

**🔧 Основные возможности:**
- 📷 Захват изображения с веб-камеры в реальном времени
- 🖼️ Загрузка изображений (JPG, PNG)
- 🎚️ Коррекция яркости
- 🖼️ Показ отдельных цветовых каналов изображения
- 🖌️ Наложение графических элементов
- 📐 Изменение размера изображения
-  

## ⚡ Быстрый старт

### Установка (из PyPI)
```bash
pip install visual-processing-app
````
### Запуск
```bash
visual-app
```

## 🛠️ Установка из исходников

### Требования
- 🐍 Python 3.7+
- 📦 pip

### Шаги установки:
1. Клонирование репозитория
```
git clone https://github.com/danvar24/Practic_work_1st_term
cd Practic_work_1st_term
```

2. Создать виртуальное окружение (ОБЯЗАТЕЛЬНО на Linux/macOS)
```
# Windows
python -m venv venv
venv\Scripts\activate
```
```
# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```
3. Установка зависимостей
```
pip install -r requirements.txt
```
4. Установка пакета 
```
pip install .
```

5. Запуск 
```
python -m visual-app.main
```

## Использование

### Основной функционал
1. **🖼️ Загрузка изображения**

    Используйте кнопку "Открыть" в меню Файл
    Поддерживаемые форматы: JPG, PNG, JPEG

2. **🎭 Цветовые каналы**
   
   Доступные режимы отображения:

    - ❤️ Красный канал (R)

    - 💚 Зеленый канал (G)

    - 💙 Синий канал (B)

3. **📏 Изменение размера**

    Алгоритм работы:

    - Введите новую ширину и высоту в пикселях

    - Нажмите "Применить" для масштабирования

4. **☀️ Коррекция яркости**

    Как использовать:

    - Укажите значение усиления (от 1 до 100)

    - Программа увеличит интенсивность всех цветов

5. **✏️ Рисование линий**

    Возможности:

    - Укажите координаты начала и конца

    - Выберите толщину линии

    - Линия рисуется зеленым цветом (RGB: 0,255,0)

6. **🔄 Сброс изменений**

    - Используйте кнопку "Сбросить изменения" для возврата к исходному изображению

## 📦 Сборка проекта

### Создание пакета
1. **Вариант А: Создание Python-пакета (.whl)
```bash
pip install build
python -m build
```
После сборки файлы .whl и .tar.gz появятся в папке dist/.

2. **Вариант B: Создание исполняемого файла (Windows)**
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name VisualApp image_editor/main.py
```

Готовый .exe будет в dist/VisualApp.exe.

3.  **Вариант C: Создание бинарника (Linux/macOS)**
```bash
pyinstaller --onefile --name visual-app image_editor/main.py
```

Готовый бинарник — dist/visual-app.

### Установка и запуск

- Из исходников
```bash
python -m image_editor.main
```
- Из собранного пакета
```bash
pip install dist/visual_processing_app-1.0.0-py3-none-any.whl
visual-app  # или vpa
```

- **Проверка установки**
```bash
pip show visual-processing-app
```

- **Удаление пакета**
```bash
pip uninstall visual-processing-app
```

- **Структура проекта**
```
VisualProcessingApp/
├── build/                 # Временные файлы сборки (автоматически создается)
│   ├── bdist.win-amd64/   # Для Windows (если использовался bdist_wheel)
│   └── lib/               # Копия Python-кода
│       └── image_editor/  # (те же файлы, что в исходниках)
│
├── dist/                  # Готовые дистрибутивы
│   ├── visual_processing_app-1.0.0-py3-none-any.whl  # Wheel-пакет
│   ├── visual_processing_app-1.0.0.tar.gz            # Исходный архив
│   └── VisualApp.exe      # Исполняемый файл (если использовался PyInstaller)
│
├── image_editor/          # Исходный код (без изменений)
│   ├── __init__.py
│   ├── __main__.py
│   └── main.py
│
├── visual_processing_app.egg-info/  # Метаданные пакета (автоматически)
│   
│   
│  
│   
│
├── LICENSE.txt            # Лицензия
├── README.md              # Документация
├── requirements.txt       # Зависимости
└── setup.py               # Конфиг сборки
```

## 📚 Зависимости 
Все зависимости указываются в requirements.txt:
- [OpenCV](https://opencv.org/) - работа с изображениями и камерой
- [Pillow](https://python-pillow.org/) - обработка графики
- [NumPy](https://numpy.org/) - математические операции

```text
opencv-python>=4.5
pillow>=9.0
numpy>=1.20
```

## ⚖️ Лицензия
Этот проект распространяется под лицензией MIT. Подробнее см. в файле LICENCE.txt.
