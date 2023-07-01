import pyautogui
import keyboard
import time

DEFAULT_INTERVAL = 0.1
DEFAULT_STATUS = "Программа запущена"
DEFAULT_START_STATUS = "Нажмите 'Начать' для начала работы программы"
DEFAULT_RESUME_STATUS = "Нажмите 'Продолжить' для возобновления работы программы"
DEFAULT_PAUSED_STATUS = "Программа поставлена на паузу"
DEFAULT_DONE_STATUS = "Работа программы завершена"
START_BUTTON = "Начать"
RESUME_BUTTON = "Продолжить работу"
PAUSE_BUTTON = "Поставить на паузу"
RESTART_BUTTON = "Начать заново"
EXIT_BUTTON = "Выйти"
OKEY_BUTTON = "Ок"
paused = False
done = False

def set_start_status():
    response = pyautogui.confirm(text=DEFAULT_START_STATUS, title="Уведомление", buttons=[START_BUTTON])
    if response == START_BUTTON:
        start_program()

def set_status(status):
    global done
    if done:
        response = pyautogui.confirm(text=status, title="Уведомление", buttons=[RESTART_BUTTON, EXIT_BUTTON])
        if response == RESTART_BUTTON:
            done = False
            set_start_status()
        else:
            exit()
    elif paused:
        response = pyautogui.confirm(text=status, title="Уведомление", buttons=[RESUME_BUTTON, OKEY_BUTTON])
        if response == RESUME_BUTTON:
            toggle_pause()
    elif "завершена" in status:
        done = True
        set_status(status)
    else:
        response = pyautogui.confirm(text=status, title="Уведомление", buttons=[PAUSE_BUTTON, OKEY_BUTTON])
        if response == PAUSE_BUTTON:
            toggle_pause()

    print(f"[+] Статус: {status}")

def start_program():
    global done
    done = False
    set_status(DEFAULT_STATUS)
    try:
        while True:
            handle_mouse()
            for key in EXIT_KEYS + PAUSE_KEYS:
                if keyboard.is_pressed(key):
                    on_key_press(key)
            time.sleep(DEFAULT_INTERVAL)
    except KeyboardInterrupt:
        set_status("Программа завершена пользователем.")
    except pyautogui.FailSafeException:
        set_status("Движение мыши привело к ошибке.")
    finally:
        set_status("Программа завершена")

def toggle_pause():
    global paused
    paused = not paused
    pause_desc = DEFAULT_PAUSED_STATUS if paused else DEFAULT_RESUME_STATUS
    set_status(pause_desc)

def on_key_press(key):
    if key in EXIT_KEYS:
        set_status("Завершение программы.")
        exit()
    if key in PAUSE_KEYS:
        toggle_pause()

def handle_mouse():
    if not paused and not done:
        x, y = pyautogui.position()
        mouse_click(x, y)

def mouse_click(x, y):
    pyautogui.click(x, y)

START_BUTTON = "Начать"
RESUME_BUTTON = "Продолжить"
PAUSE_BUTTON = "Пауза"
RESTART_BUTTON = "Начать заново"
EXIT_BUTTON = "Выйти"
PAUSE_KEYS = ["tab"]
EXIT_KEYS = ["esc"]

def main():
    set_start_status()

if __name__ == "__main__":
    main()