import pyautogui
import keyboard
import time

DEFAULT_INTERVAL = 0.1
DEFAULT_STATUS = "Программа запущена"
DEFAULT_PAUSED_STATUS = "Пауза в работе программы"
DEFAULT_UNPAUSED_STATUS = "Продолжение работы программы"
PAUSE_KEYS = ["tab"]
EXIT_KEYS = ["esc"]
paused = False

def mouse_click(x, y):
    pyautogui.click(x, y)

def set_status(status):
    print(f"[+] Статус: {status}")
    if paused:
        pyautogui.alert(status, title="Уведомление")
    elif "завершена" in status:
        response = pyautogui.confirm(text=status, title="Уведомление", buttons=["Запустить заново", "Выйти"])
        if response == "Запустить заново":
            main()
        else:
            exit()

def toggle_pause():
    global paused
    paused = not paused
    pause_desc = DEFAULT_PAUSED_STATUS if paused else DEFAULT_UNPAUSED_STATUS
    set_status(pause_desc)

def on_key_press(key):
    if key in EXIT_KEYS:
        set_status("Завершение программы.")
        exit()
    if key in PAUSE_KEYS:
        toggle_pause()

def handle_mouse():
    if not paused:
        x, y = pyautogui.position()
        mouse_click(x, y)

def main():
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
        set_status("Программа завершена. Нажмите 'Запустить заново' чтобы перезапустить программу, или 'Выйти'.")
        pyautogui.alert("Программа завершена.", title="Уведомление", buttons=["Запустить заново", "Выйти"])     

if __name__ == "__main__":
    main()