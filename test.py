# The MIT License (MIT)
#
# Copyright (c) 2025 Team "Фрикодеры"
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


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

def on_activity():
    """Сбрасывает таймер бездействия и включает монитор при обнаружении активности пользователя."""
    global last_active_time
    last_active_time = time.time()
    monitor_on()

def detect_face():
    """Использует веб-камеру для обнаружения лица пользователя."""
    global last_face_detected_time

    cap = cv2.VideoCapture(0)  # Открываем веб-камеру
    ret, frame = cap.read()  # Читаем кадр

    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Преобразуем изображение в черно-белое
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
        if len(faces) > 0:
            last_face_detected_time = time.time()  # Обновляем время обнаружения лица

    cap.release()  # Закрываем веб-камеру

# Запуск слушателей клавиатуры и мыши
mouse_listener = mouse.Listener(on_move=lambda x, y: on_activity(),
                                on_click=lambda x, y, button, pressed: on_activity())
keyboard_listener = keyboard.Listener(on_press=lambda key: on_activity())

mouse_listener.start()
keyboard_listener.start()

while True:
    detect_face()  # Проверяем наличие лица через веб-камеру

    if get_idle_time() > IDLE_THRESHOLD or (time.time() - last_face_detected_time > FACE_DETECTION_THRESHOLD):
        monitor_off()  # Отключаем монитор, если пользователь неактивен или его нет перед камерой

    time.sleep(10)  # Проверяем каждые 10 секунд