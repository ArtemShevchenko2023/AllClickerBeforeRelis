# Импорты должны быть в первой части кода
import pyautogui
import keyboard
import time

# Задаем константы с понятными именами
START_BUTTON = "Начать"
RESUME_BUTTON = "Выключить паузу"
PAUSE_BUTTON = "Включить паузу"
RESTART_BUTTON = "Начать заново"
EXIT_BUTTON = "Продолжить"
PAUSE_KEYS = ["tab"]
EXIT_KEYS = ["esc"]

DEFAULT_INTERVAL = 0.1
DEFAULT_STATUS = "Программа запущена"
DEFAULT_START_STATUS = "Нажмите 'Начать' для начала работы программы"
DEFAULT_RESUME_STATUS = "Нажмите 'Продолжить' для возобновления работы программы"
DEFAULT_PAUSED_STATUS = "Программа поставлена на паузу"
DEFAULT_DONE_STATUS = "Работа программы завершена"

paused = False
done = False

# Добавляем документацию и комментарии к функциям
def set_start_status():
    """
    Выводит уведомление с просьбой начать программу.
    """
    response = pyautogui.confirm(text=DEFAULT_START_STATUS, title="Уведомление", buttons=[START_BUTTON])
    if response == START_BUTTON:
        start_program()

def set_status(status):
    """
    Выводит уведомление с новым статусом и инструкцией для пользователя.
    """
    global done
    if done:
        response = pyautogui.confirm(text=status, title="Уведомление", buttons=[RESTART_BUTTON, EXIT_BUTTON])
        if response == RESTART_BUTTON:
            done = False
            set_start_status()
        else:
            exit()
    elif paused:
        response = pyautogui.confirm(text=status, title="Уведомление", buttons=[RESUME_BUTTON, EXIT_BUTTON])
        if response == RESUME_BUTTON:
            toggle_pause()
    elif "завершена" in status:
        done = True
        set_status(status)
    else:
        response = pyautogui.confirm(text=status, title="Уведомление", buttons=[PAUSE_BUTTON, EXIT_BUTTON])
        if response == PAUSE_BUTTON:
            toggle_pause()

    print(f"[+] Статус: {status}")

def start_program():
    """
    Запускает программу и проверяет, была ли нажата кнопка выхода.
    """
    global done
    done = False
    set_status(DEFAULT_STATUS)
    try:
        while True:
            handle_mouse()
            for key in EXIT_KEYS + PAUSE_KEYS:
                if keyboard.is_pressed(key):
                    on_key_press(key)
                    # Проверяем, что кнопка нажата только при запущенной программе
                    if done:
                        break
            time.sleep(DEFAULT_INTERVAL)
    except KeyboardInterrupt:
        set_status("Программа завершена пользователем.")
    except pyautogui.FailSafeException:
        set_status("Движение мыши привело к ошибке.")
    finally:
        set_status(DEFAULT_DONE_STATUS)

def toggle_pause():
    """
    Паузит/возобновляет программу.
    """
    global paused
    paused = not paused
    pause_desc = DEFAULT_PAUSED_STATUS if paused else DEFAULT_RESUME_STATUS
    set_status(pause_desc)

def on_key_press(key):
    """
    Обрабатывает нажатия кнопок выхода и паузы.
    """
    if key in EXIT_KEYS:
        set_status("Завершение программы.")
        exit()
    if key in PAUSE_KEYS:
        toggle_pause()

def handle_mouse():
    """
    Обрабатывает движение мыши, проводит клики.
    """
    if not paused and not done:
        x, y = pyautogui.position()
        mouse_click(x, y)

def mouse_click(x, y):
    """
    Проводит клик на местоположением x, y.
    """
    pyautogui.click(x, y)


# ПОВЫШЕНИЕ МОДУЛЬНОСТИ
def prompt_start():
    """
    Отображает уведомление для начала программы.
    """
    response = pyautogui.confirm(text=DEFAULT_START_STATUS, title="Уведомление", buttons=[START_BUTTON])
    if response == START_BUTTON:
        run_program()

def run_program():
    """
    Запускает главный цикл программы для кликов мышью.
    """
    global done
    done = False
    set_status(DEFAULT_STATUS)
    try:
        while True:
            handle_mouse()
            check_system_keys()
            time.sleep(DEFAULT_INTERVAL)
    except KeyboardInterrupt:
        set_status("Программа завершена пользователем.")
    except pyautogui.FailSafeException:
        set_status("Движение мыши привело к ошибке.")
    finally:
        set_status(DEFAULT_DONE_STATUS)

def check_system_keys():    
    """
    Обрабатывает нажатия кнопок выхода и паузы.
    """
    global done
    for key in EXIT_KEYS + PAUSE_KEYS:
        if keyboard.is_pressed(key):
            on_key_press(key)
            # Проверяем, что кнопка нажата только при запущенной программе
            if done:
                break

def main():
    prompt_start()

if __name__ == "__main__":
    main()