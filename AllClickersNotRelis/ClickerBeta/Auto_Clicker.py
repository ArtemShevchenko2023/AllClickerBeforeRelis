import pyautogui
import keyboard
paused = False
while True: 
    try: 
        x, y = pyautogui.position()
        if not paused:
            pyautogui.click(x, y)
        if keyboard.is_pressed('esc'):
            print("Вы нажали клавишу Esc, программа завершит работу.")
            break
        if keyboard.is_pressed('tab'):
            keyboard.release('tab')
            if not paused:
                print("Программа поставлена на паузу.")
                paused = True
            else:
                print("Продолжаем работу.")
                paused = False
        pyautogui.sleep(0.1)
    except KeyboardInterrupt:
        print('Вы завершили программу.')
        break