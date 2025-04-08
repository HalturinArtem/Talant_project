# Тестовый файл

import os
import time
import platform
import ctypes
import cv2 # Библиотека OpenCV для работы с веб-камерой
from pynput import mouse, keyboard # Библиотека для отслеживания клавиатуры и мыши

# Время бездействия в секундах перед выключением монитора
IDLE_THRESHOLD = 30
FACE_DETECTION_THRESHOLD = 5 # Время (в секундах), после которого выключится монитор, если нет лица
OS_TYPE = platform.system()
last_active_time = time.time() # Время последней активности
last_face_detected_time = time.time()  # Время последнего обнаруженного лица

# Указываем полный путь до файла каскада
CASCADE_PATH = r'haar_metod/haarcascade_frontalface_default.xml'

# Загружаем каскадный классификатор для распознавания лиц
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def get_idle_time():
    """Возвращает время (в секундах) с момента последней активности пользователя."""
    global last_active_time
    return time.time() - last_active_time
    face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def monitor_on():
    """Включает монитор при обнаружении активности пользователя."""
    if OS_TYPE == "Windows":
        ctypes.windll.user32.SendMessageW(0xFFFF, 0x0112, 0xF170, -1)
    elif OS_TYPE == "Linux":
        os.system("xset dpms force on")
