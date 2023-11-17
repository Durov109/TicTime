import PySimpleGUI as sg
import time

time.sleep(0.6)

def time_as_int():
    return int(round(time.time() * 100))

# ----------------  Создаем графическое окно  ----------------
# что будет внутри окна
# первым описываем кнопку и сразу указываем размер шрифта
layout = [[sg.Button('Старт', enable_events=True, key='-START-STOP-', font='Helvetica 16')],
        # затем делаем текст
        [sg.Text('Время:', size=(25, 1), key='-text_1-', font='Helvetica 16')],
        #[sg.Text('Всего:', size=(25, 1), key='-text_2-', font='Helvetica 16')],
        [sg.Text('Общее время:', size=(25, 1), key='-text_3-', font='Helvetica 16')]]

# рисуем окно
window = sg.Window('Таймер', layout, size=(750,160))

current_time, paused_time, paused = 0, 0, False
start_time = time_as_int()

#-----------------Переменная для вывода в окно (Всего:)---------------------
out_time = None
#Открываем файл для чтения (или указываем путь как указано в 56 строке!!!)
try:
    with open('Total.txt' , 'r', encoding='utf-8') as file_for_window:
        step1 = file_for_window.read().strip().split()
        out_time = f"{step1[0]} ч. {step1[2]} м. {step1[4]} с."
    print(out_time)
except:
    out_time = 'Нету данных'
#--------------------------------------------------------------

while True:
    # --------- Чтение и обновление окна --------
    if not paused:
        #Обновление значений каждые 10 милисекунд
        event, values = window.read(timeout=10)
        current_time = time_as_int() - start_time

    else:
        event, values = window.read()   
    
    # --------- Выполнение операций кнопками --------
    if event in (sg.WIN_CLOSED, 'Exit'):

        #---------------------------------------------Переменные для записи в файл------------------------------------------------------
        """Открываем файл Timer в режиме запись и добавление данных и открываем файл Total в режиме удалить данные и внести новые"""
        with open('Timer.txt', 'a+', encoding='utf-8') as file_timer, open('Total.txt' , 'w', encoding='utf-8') as file_total:
            """
            Файлы создадутся сами там где находится программа или вводим путь сами
            Пример: open('C:\\Users\\admin\\Desktop\\Timer.txt', 'a+', encoding='utf-8')    
            """

            #Добавляем время в файл Timer
            print(str('{:02d}:{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 3600,(current_time // 100) // 60 % 60,(current_time // 100) % 60, current_time % 100)), file=file_timer)
            #Делаем перенос на 1 строку (Обязательно!!! Иначе будет считываться всё остальное кроме 1 строки)
            file_timer.seek(0)

            hour = 0
            minute = 0
            second = 0

            for i in file_timer:
                i = i.strip().split(":")
                hour += int(i[0])
                minute += int(i[1])
                second += int(float((i[2])))

                if second > 60 or minute > 60:
                    if second > 60:
                        minute_uravnenie = second//60
                        second_uravnenie = second%60

                        second = second_uravnenie
                        minute += minute_uravnenie

                elif minute > 60:
                    hour_uravnenie = minute//60
                    minute_uravnenie = minute%60

                    minute = minute_uravnenie
                    hour += hour_uravnenie
    
            print(f"{str(hour)} час(а/ов) {str(minute)} минут(ы) {str(second)} секунд(ы)", file=file_total)
        #---------------------------------------------------------------------------------------------------------------------------------------------------

        break
    
    elif event == '-START-STOP-':
        paused = not paused

        if paused==True:
            paused_time = time_as_int()
            print(f"Время: {'{:02d}:{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 3600,(current_time // 100) // 60 % 60,(current_time // 100) % 60, current_time % 100)}")

        else:
            start_time = start_time + time_as_int() - paused_time

        # Обновление старта и стопа
        window['-START-STOP-'].update('Старт' if paused else 'Стоп')

    # --------- Вывод времени на дисплей --------
    #window['-text_1-'].update(f"Время: {'{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,(current_time // 100) % 60,current_time % 100)}")
    # window['text'].update('{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 60,
    #                                                     (current_time // 100) % 60,
    #                                                     current_time % 100))
    window['-text_1-'].update(f"Время: {'{:02d}:{:02d}:{:02d}.{:02d}'.format((current_time // 100) // 3600,(current_time // 100) // 60 % 60,(current_time // 100) % 60, current_time % 100)}")
    window['-text_3-'].update(f"Общее время: {out_time}")


window.close()