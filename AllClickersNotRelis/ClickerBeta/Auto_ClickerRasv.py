import pyautogui
import keyboard

paused = False

while True: 
    try: 
        # Получаем координаты курсора
        x, y = pyautogui.position()

        if not paused:
            # Если не находится на паузе, кликаем по координатам курсора
            pyautogui.click(x, y)

        # Проверяем, нажата ли клавиша "Esc"
        if keyboard.is_pressed('esc'):
            print("Вы нажали клавишу Esc, программа завершит работу.")
            break

        # Проверяем, нажата ли клавиша "Tab"
        if keyboard.is_pressed('tab'):
            keyboard.release('tab')
            if not paused:
                # Если не на паузе, сообщаем об этом и ставим программу на паузу
                print("Программа поставлена на паузу.")
                paused = True
            else:
                # Если на паузе, сообщаем об этом и возобновляем работу
                print("Продолжаем работу.")
                paused = False

        # Делаем задержку в 0.1 секунду
        pyautogui.sleep(0.1)

    except KeyboardInterrupt:
        print('Вы завершили программу.')
        break