from setuptools import setup, find_packages
from pathlib import Path

# Автоматическое чтение версии из __init__.py
version = "1.0.0"
try:
    with open(Path(__file__).parent / "image_editor" / "__init__.py", encoding="utf-8") as f:
        for line in f:
            if line.startswith("__version__"):
                version = line.split("=")[1].strip().strip('"\'')
except:
    pass

# Чтение README для описания
try:
    with open("README.md", encoding="utf-8") as f:
        long_description = f.read()
except:
    long_description = "Графический редактор изображений с поддержкой веб-камеры"

setup(
    name="visual-processing-app",
    version=version,
    author="Тюменцев Роман",
    author_email="romatumencev5128@email.com",
    description="Приложение для обработки изображений",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ram3ndev/ImageProcessingApp",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.5",
        "Pillow>=9.0",
        "numpy>=1.20"
    ],
    entry_points={
        "console_scripts": [
            "visual-app=image_editor.main:main",
            "vpa=image_editor.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
)