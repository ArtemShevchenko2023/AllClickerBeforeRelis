import pyautogui
import keyboard
import time

START_BUTTON = "Начать"
PAUSE_BUTTON = "Поставить на паузу"
RESUME_BUTTON = "Возобновить"
STOP_BUTTON = "Остановить"
RESTART_BUTTON = "Начать заново"
EXIT_BUTTON = "Закрыть"

DEFAULT_INTERVAL = 0.1
DEFAULT_STATUS = "Программа запущена"
DEFAULT_PAUSED_STATUS = "Программа приостановлена"
DEFAULT_DONE_STATUS = "Работа программы завершена"
DEFAULT_START_STATUS = "Нажмите 'Начать' для начала работы программы"

paused = False

def prompt_start():
    create_start_box()
    run_program()

def create_start_box():
    response = pyautogui.confirm(text=DEFAULT_START_STATUS, title="Начало работы", buttons=[START_BUTTON])
    if response != START_BUTTON:
        create_start_box()

def create_pause_box():
    dialog_result = pyautogui.confirm(text=DEFAULT_PAUSED_STATUS, title="Программа приостановлена", buttons=[RESUME_BUTTON, EXIT_BUTTON])
    if dialog_result == RESUME_BUTTON:
        toggle_pause()
    elif dialog_result == EXIT_BUTTON:
        terminate_program()

def create_restart_box():
    dialog_result = pyautogui.confirm(text="Начать заново?", title="Перезапуск программы", buttons=[RESTART_BUTTON, EXIT_BUTTON])
    if dialog_result == RESTART_BUTTON:
        restart_program()
    elif dialog_result == EXIT_BUTTON:
        terminate_program()

def create_stop_box():
    response = pyautogui.confirm(text="Вы останавливаете работу программы!", title="Останов работы программы", buttons=[STOP_BUTTON, RESTART_BUTTON, EXIT_BUTTON])
    if response == STOP_BUTTON:
        terminate_program()
    elif response == RESTART_BUTTON:
        restart_program()
    elif response == EXIT_BUTTON:
        terminate_program()

def run_program():
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
    global paused
    if keyboard.is_pressed("tab") or pyautogui.confirm(text=DEFAULT_PAUSED_STATUS, title="Программа приостановлена", buttons=[RESUME_BUTTON, PAUSE_BUTTON]) == PAUSE_BUTTON:
        toggle_pause()
    for key in keyboard.alphanumeric_key_names:
        if keyboard.is_pressed(key):
            on_key_press(key)

def set_status(status):
    if "завершена" in status:
        create_stop_box()
    elif paused:
        create_pause_box()
    else:
        create_restart_box()

    print(f"[+] Статус: {status}")

def on_key_press(key):
    if key == "esc":
        create_stop_box()

def handle_mouse():
    if not paused:
        x, y = pyautogui.position()
        mouse_click(x, y)

def mouse_click(x, y):
    pyautogui.click(x, y)

def toggle_pause():
    global paused
    paused = not paused

def restart_program():
    global paused
    paused = False
    run_program()

def terminate_program():
    global paused
    paused = False
    done = True

def main():
    prompt_start()

if __name__ == "__main__":
    main()
#ПРИМЕЧАНИЕ!!!!!!! Эта версия в разработке и пока что неспособна работать корректно!!!