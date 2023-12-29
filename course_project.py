from tkinter import *
import random
import time
import copy
import os
from tkinter import messagebox
from tkinter import font
from tkinter.messagebox import showinfo, showerror
import hashlib

spisok_hodov=()#конечный список ходов компьютера
predict_hodov=3#сколько ходов компьютер предсказывает
k_rezult=0
o_rezult=0
poz1_x=-1#клетка не определена
f_hodigroka=True#определение хода игрока, по умолчанию активен игрок

def hash_password(password): # Хеширование пароля
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def check_login(): # Проверяем наличие логина в файле
    if os.path.exists("users.txt"):
        file = open("users.txt", "r+")
        with open("users.txt", "r") as file:
            lines = file.readlines()
            login_input = login.get()
            for line in lines:
                if login_input in line:
                    return True
        return False

def check_users(): # Проверяем наличие данных в файле о пользователе
    if os.path.exists("users.txt"):
        file = open("users.txt", "r+")
        lines = file.readlines()
        login_input = login.get()
        password_input = password.get()
        for line in lines:
            parts = line.strip().split(':')
            if len(parts) == 2:
                stored_login, stored_password = parts
                if login_input == stored_login and hash_password(password_input) == stored_password:
                    return True
        return False
    
def registration_user(): # Регистрируем пользователя
    if not login.get() or not password.get():
        showerror("Ошибка", "Поля 'Логин' и 'Пароль' должны быть заполнены.")
    elif check_login():
        showerror("Ошибка", "Учетная запись с таким логином уже существует.")
    else:
        with open("users.txt", "a") as file:
            file.write(f"{login.get()}:{hash_password(password.get())}\n")
        root.destroy()
        showinfo("Успех", "Регистрация успешно завершена.\nПри следующем входе введите свои данные, чтобы войти в игру!")

def enter_users():
    if check_users(): #если такой пользователь существует
        showinfo("Успех!", "Вы вошли в свой аккаунт")        
        main_window=Toplevel()
        main_window.title('Шашки царские башни')
        doska=Canvas(main_window, width=800,height=800,bg='#FFFFFF')
        doska.pack()

        def checkers_images():#загружаем шашки
            global checkers
            i1=PhotoImage(file="checkers_images\\white.gif")
            i2=PhotoImage(file="checkers_images\\white_king.gif")
            i3=PhotoImage(file="checkers_images\\black.gif")
            i4=PhotoImage(file="checkers_images\\black_king.gif")
            i5=PhotoImage(file="checkers_images\\qween_shashki.png")
            i6=PhotoImage(file="checkers_images\\qween_shashkib.png")
            checkers=[0,i1,i2,i3,i4,i5,i6]
    
        def new_game():#начинаем новую партию игры
            global pole
            pole=[[0,3,0,6,0,3,0,3],
                [3,0,3,0,3,0,3,0],
                [0,3,0,3,0,3,0,3],
                [0,0,0,0,0,0,0,0],
                [0,0,0,0,0,0,0,0],
                [1,0,1,0,1,0,1,0],
                [0,1,0,1,0,1,0,1],
                [1,0,1,0,5,0,1,0]]
            
        def draw_board(x_poz_1,y_poz_1,x_poz_2,y_poz_2):#рисуем шашечную доску
            global checkers
            global pole
            global red_outline,green_outline
            k=100
            x=0
            doska.delete('all')
            red_outline=doska.create_rectangle(-5, -5, -5, -5,outline="red",width=5)
            green_outline=doska.create_rectangle(-5, -5, -5, -5,outline="green",width=5)
        
            while x<8*k:
                y=1*k
                while y<8*k:
                    doska.create_rectangle(x, y, x+k, y+k,fill="#292424")
                    y+=2*k
                x+=2*k
            x=1*k
            while x<8*k:
                y=0
                while y<8*k:
                    doska.create_rectangle(x, y, x+k, y+k,fill="#292424")
                    y+=2*k
                x+=2*k
            
            for y in range(8):#распологаем шашки
                for x in range(8):
                    z=pole[y][x] #проходимся по строкам [y] и столбцам [x]
                    if z:  
                        if (x_poz_1,y_poz_1)!=(x,y):#стоячие шашки
                            doska.create_image(x*k,y*k, anchor=NW, image=checkers[z])

            #рисуем активную шашку         
            z=pole[y_poz_1][x_poz_1]
            if z: #если позиция не равна 0, т. е. есть шашка
                doska.create_image(x_poz_1*k,y_poz_1*k, anchor=NW, image=checkers[z],tag='ani')

            #анимация шашек
            kx = 1 if x_poz_1<x_poz_2 else -1
            ky = 1 if y_poz_1<y_poz_2 else -1
            for i in range(abs(x_poz_1-x_poz_2)):#анимация движения шашки
                for ii in range(33):
                    doska.move('ani',0.03*k*kx,0.03*k*ky)
                    doska.update()
                    time.sleep(0.01)

        def message_output(mes): # выводим сообщение об окончании игры 
            global f_hodigroka
            title='Игра завершена'
            if mes==1:
                i=messagebox.showinfo(title=title, message='Вы победили!\nХотите переиграть?',icon='info')
            if mes==2:
                i=messagebox.showinfo(title=title, message='Вы проиграли!\nХотите переиграть?',icon='info')
            if mes==3:
                i=messagebox.showinfo(title=title, message='Ходов больше нет.\nХотите переиграть?',icon='info')
            if i:
                new_game()
                draw_board(-1,-1,-1,-1)#рисуем игровое поле
                f_hodigroka=True #игрок может делать ход



        def position_one(event):#определяем клетку для хода 1
            x,y=(event.x)//100,(event.y)//100#вычисляем координаты клетки
            doska.coords(green_outline,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке


        def position_two(event):#определяем клетку для хода 2
            global poz1_x,poz1_y,poz2_x,poz2_y
            global f_hodigroka
            x,y=(event.x)//100,(event.y)//100#определяем координаты клетки
            if pole[y][x]==1 or pole[y][x]==2 or pole[y][x]==5:#если шашка игрока в выбранной клетке
                doska.coords(red_outline,x*100,y*100,x*100+100,y*100+100)#рамка в выбранной клетке
                poz1_x,poz1_y=x,y
            else:
                if poz1_x!=-1:#клетка выбрана
                    poz2_x,poz2_y=x,y
                    if f_hodigroka:#если ход игрока
                        igrok_move()
                        if not(f_hodigroka):#если ход компьютера
                            time.sleep(0.5)
                            computers_move()#передаём ход компьютеру
                            
                    poz1_x=-1#клетка не определена
                    doska.coords(red_outline,-5,-5,-5,-5)#рамка вне поля   

        def computers_move():
            global f_hodigroka
            global spisok_hodov
            check_computer_movement(1,(),[])
            if spisok_hodov:#проверяем наличие доступных ходов
                kol_hodov=len(spisok_hodov)#вычисляем количество доступных ходов в списке `spisok_hodov` и сохраняем его в переменной
                tek_hod=random.randint(0,kol_hodov-1)#генерируем случайное целое число в диапазоне от 0 до `kol_hodov-1` и сохраняем его в переменной. Это число будет использоваться для выбора случайного хода из списка `spisok_hodov`
                deep_hod=len(spisok_hodov[tek_hod])#вычисляем длину выбранного случайного хода из списка `spisok_hodov`
                for i in range(deep_hod-1):
                    #выполняем ход
                    move_checkers(1,spisok_hodov[tek_hod][i][0],spisok_hodov[tek_hod][i][1],spisok_hodov[tek_hod][1+i][0],spisok_hodov[tek_hod][1+i][1])
                spisok_hodov=[]#очищаем список ходов
                f_hodigroka=True#игрок может делать ход
            
            s_komp_checkers,s_igrok_checkers,s_iqween,s_kqween=checkers_counting()
            if not(s_igrok_checkers) or not(s_iqween) or check_victory_komputer():
                message_output(2)
            elif not(s_komp_checkers) or not(s_kqween) or check_victory_igrok():
                message_output(1)
            elif f_hodigroka and not(spisok_hodov_igroka()):
                message_output(3)
            elif not(f_hodigroka) and not(spisok_hodov_komp()):
                message_output(3)


        def spisok_hodov_komp():#генерируем список ходов компьютера
            spisok=check_hod_komp1([])#проверяем обязательные ходы
            if not(spisok):
                spisok=check_hod_komp2([])#проверяем оставшиеся ходы
            return spisok
        
        def check_computer_movement(tek_hod,n_spisok,spisok):#!!!
            global pole
            global spisok_hodov
            global best_rezult,k_rezult,o_rezult
            if not(spisok):#если список ходов пустой...
                spisok=spisok_hodov_komp()#заполняем
        
            if spisok:
                k_pole=copy.deepcopy(pole)
                for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проходим по всем ходам из списка
                    tek_spisok_hod=move_checkers(0,poz1_x,poz1_y,poz2_x,poz2_y)
                    if tek_spisok_hod:#если существует ещё ход
                        check_computer_movement(tek_hod,(n_spisok+((poz1_x,poz1_y),)),tek_spisok_hod)
                    else:
                        check_igrok_movement(tek_hod,[])
                        if tek_hod==1:
                            t_rez=o_rezult/k_rezult
                            if not(spisok_hodov):#записываем если пустой
                                spisok_hodov=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                                best_rezult=t_rez#записываем лучший результат
                            else:
                                if t_rez==best_rezult:
                                    spisok_hodov=spisok_hodov+(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                                if t_rez>best_rezult:
                                    spisok_hodov=()
                                    spisok_hodov=(n_spisok+((poz1_x,poz1_y),(poz2_x,poz2_y)),)
                                    best_rezult=t_rez#записываем лучший результат
                            o_rezult=0
                            k_rezult=0
        
                    pole=copy.deepcopy(k_pole)#возвращаем поле
            else:
                s_komp_checkers,s_igrok_checkers,s_iqween,s_kqween=checkers_counting()#подсчёт результата хода
                o_rezult+=(s_komp_checkers+s_kqween-s_igrok_checkers-s_iqween)
                k_rezult+=1

        def checkers_counting():#подсчёт шашек на поле
            global pole

            s_igrok_checkers=0
            s_iqween = 0

            s_komp_checkers=0
            s_kqween = 0

            for i in range(8):
                for ii in pole[i]:
                    if ii==1:s_igrok_checkers+=1
                    if ii==5:s_iqween+=1
                    if ii==2:s_igrok_checkers+=3
                    if ii==3:s_komp_checkers+=1
                    if ii==6:s_kqween+=1
                    if ii==4:s_komp_checkers+=3
            return s_komp_checkers,s_igrok_checkers,s_iqween,s_kqween

        def check_victory_igrok():
            global pole
            player_queen_position = None  # позиция царской шашки игрока

            # Поиск позиций царских шашек игрока и врага
            for i in range(8):
                for j in range(8):
                    if pole[i][j] == 5:
                        player_queen_position = (i, j)

            # Проверка, достигла ли царская шашка игрока противоположной горизонтали на одну из четырех клеток
            if player_queen_position[0] == 0:
                return True
            return False
            
        def check_victory_komputer():
            global pole
            enemy_queen_position = None  # позиция царской шашки врага

            # Поиск позиций царских шашек игрока и врага
            for i in range(8):
                for j in range(8):
                    if pole[i][j] == 6:
                        enemy_queen_position = (i, j)

            # Проверка, достигла ли царская шашка врага противоположной горизонтали на одну из четырех клеток
            if enemy_queen_position is not None and enemy_queen_position[0] == 7:
                return True
            return False

        def igrok_move():
            global poz1_x,poz1_y,poz2_x,poz2_y
            global f_hodigroka
            f_hodigroka=False#считаем ход игрока выполненным
            spisok=spisok_hodov_igroka()
            if spisok:
                if ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok:#проверяем ход на соблюдение правил игры
                    tek_spisok_hod=move_checkers(1,poz1_x,poz1_y,poz2_x,poz2_y)#если всё хорошо, делаем перемещаем шашку            
                    if tek_spisok_hod:#если есть ещё ход той же шашкой
                        f_hodigroka=True#считаем ход игрока невыполненным
                else:
                    f_hodigroka=True#считаем ход игрока невыполненным
            doska.update()
            s_komp_checkers,s_igrok_checkers,s_iqween,s_kqween=checkers_counting()
            if not(s_igrok_checkers) or not(s_iqween) or check_victory_komputer():
                message_output(2)
            elif not(s_komp_checkers) or not(s_kqween) or check_victory_igrok():
                message_output(1)
            elif f_hodigroka and not(spisok_hodov_igroka()):
                message_output(3)
            elif not(f_hodigroka) and not(spisok_hodov_komp()):
                message_output(3)

        def spisok_hodov_igroka():#составляем список ходов игрока
            spisok=check_hod_igrok1([])#проверяем обязательные ходы
            if not(spisok):
                spisok=check_hod_igrok2([])#проверяем оставшиеся ходы
            return spisok

        def check_hod_igrok1(spisok):#проверка наличия обязательных ходов
            spisok=[]#список ходов
            for y in range(8):#сканируем всё поле
                for x in range(8):
                    spisok=check_hod_igrok1p(spisok,x,y)
            return spisok

        def check_hod_igrok1p(spisok,x,y):
            if pole[y][x]==1 or pole[y][x]==5:#шашки
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                        if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4 or pole[y+iy][x+ix]==6:
                            if pole[y+iy+iy][x+ix+ix]==0:
                                spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
            if pole[y][x]==2:#шашка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    true_move=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if true_move==1:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or pole[y+iy*i][x+ix*i]==6:
                                true_move+=1 # увеличиваем на 1, если на пути встречается вражеская фигура
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or pole[y+iy*i][x+ix*i]==5 or true_move==2: #если на пути встречается своя фигура, то...
                                if true_move>0:spisok.pop()#...удаляем ход из списка
                                break
            return spisok


        def check_hod_igrok2(spisok):#проверка наличия остальных ходов
            for y in range(8):#сканируем всё поле
                for x in range(8):
                    if pole[y][x]==1 or pole[y][x]==5:#шашки
                        for ix,iy in (-1,-1),(1,-1):
                            if 0<=y+iy<=7 and 0<=x+ix<=7:
                                if pole[y+iy][x+ix]==0:
                                    spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                                if pole[y+iy][x+ix]==3 or pole[y+iy][x+ix]==4 or pole[y+iy][x+ix]==6:
                                    if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                        if pole[y+iy*2][x+ix*2]==0:
                                            spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
                    if pole[y][x]==2:#шашка с короной
                        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                            true_move=0#определение правильности хода
                            for i in range(1,8):
                                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                                    if pole[y+iy*i][x+ix*i]==0:
                                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or pole[y+iy*i][x+ix*i]==6:
                                        true_move+=1
                                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or pole[y+iy*i][x+ix*i]==5 or true_move==2:
                                        break
            return spisok
            
        def check_igrok_movement(tek_hod,spisok):
            global pole,k_rezult,o_rezult
            global predict_hodov
            if not(spisok):
                spisok=spisok_hodov_igroka()
        
            if spisok:#проверяем наличие доступных ходов
                k_pole=copy.deepcopy(pole)#копируем поле
                for ((poz1_x,poz1_y),(poz2_x,poz2_y)) in spisok: # перебираем каждый возможный ход в списке                     
                    tek_spisok_hod=move_checkers(0,poz1_x,poz1_y,poz2_x,poz2_y)
                    if tek_spisok_hod:#если существует ещё ход,...
                        check_igrok_movement(tek_hod,tek_spisok_hod) #... то рекурсивно вызываем функцию для проверки остальных ходов
                    else: # если ходов больше нет
                        if tek_hod<predict_hodov: # если текущий ход меньше максимального количества ходов predict_hodov
                            check_computer_movement(tek_hod+1,(),[])
                        else:
                            s_komp_checkers,s_igrok_checkers,s_kqween,s_iqween=checkers_counting()#подсчёт результата хода
                            o_rezult+=(s_komp_checkers+s_kqween-s_igrok_checkers-s_iqween)
                            k_rezult+=1
        
                    pole=copy.deepcopy(k_pole)#возвращаем поле
            else:#доступных ходов нет
                s_komp_checkers,s_igrok_checkers,s_kqween,s_iqween=checkers_counting()#подсчёт результата хода
                o_rezult+=(s_komp_checkers+s_kqween-s_igrok_checkers-s_iqween)
                k_rezult+=1


        def move_checkers(f,poz1_x,poz1_y,poz2_x,poz2_y):
            global pole
            if f:draw_board(poz1_x,poz1_y,poz2_x,poz2_y)#рисуем игровое поле
            #превращение
            if poz2_y==0 and pole[poz1_y][poz1_x]==1:
                pole[poz1_y][poz1_x]=2
            if poz2_y==7 and pole[poz1_y][poz1_x]==3:
                pole[poz1_y][poz1_x]=4
        
            pole[poz2_y][poz2_x]=pole[poz1_y][poz1_x]
            pole[poz1_y][poz1_x]=0
        
            #уничтожаем шашку игрока
            kx=ky=1
            if poz1_x<poz2_x: # если координаты x позиции начальной шашки меньше координаты x позиции конечной шашки
                kx=-1
            if poz1_y<poz2_y: # если координаты y позиции начальной шашки меньше координаты y позиции конечной шашки
                ky=-1
            x_poz,y_poz=poz2_x,poz2_y # переменные x_poz и y_poz устанавливаются равными координатам конечной позиции шашки
            while (poz1_x!=x_poz) or (poz1_y!=y_poz): # цикл будет выполняться до тех пор, пока координаты начальной и конечной позиции шашки не станут равными
                x_poz+=kx
                y_poz+=ky
                # перебираем все клетки на пути атакующей шашки от начальной до конечной позиции
                if pole[y_poz][x_poz]!=0: # если текущая клетка на игровом поле не пуста, то она считается занятой шашкой противника...
                    pole[y_poz][x_poz]=0 #...эта шашка удаляется из игры 
                    if f:draw_board(-1,-1,-1,-1)#рисуем игровое поле
                    #проверяем ход той же шашкой...
                    if pole[poz2_y][poz2_x]==3 or pole[poz2_y][poz2_x]==4 or pole[poz2_y][poz2_x]==6:#...компьютера
                        return check_hod_komp1p([],poz2_x,poz2_y)#возвращаем список доступных ходов
                    elif pole[poz2_y][poz2_x]==1 or pole[poz2_y][poz2_x]==2 or pole[poz2_y][poz2_x]==5:#...игрока
                        return check_hod_igrok1p([],poz2_x,poz2_y)#возвращаем список доступных ходов
            if f:draw_board(poz1_x,poz1_y,poz2_x,poz2_y)#рисуем игровое поле

        def check_hod_komp1(spisok):#проверка наличия обязательных ходов  # возвращает список возможных ходов для всех шашек компьютера.
            for y in range(8):#сканируем всё поле
                for x in range(8):
                    spisok=check_hod_komp1p(spisok,x,y)
            return spisok
        
        def check_hod_komp1p(spisok,x,y):
            if pole[y][x]==3 or pole[y][x]==6:#шашки
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    if 0<=y+iy+iy<=7 and 0<=x+ix+ix<=7:
                        if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2 or pole[y+iy][x+ix]==5: # проверяем возможность "перепрыгнуть" через вражескую шашку
                            if pole[y+iy+iy][x+ix+ix]==0: # понимаем, что есть возможность сделать ход, так как клетка равна 0
                                spisok.append(((x,y),(x+ix+ix,y+iy+iy)))#запись хода в конец списка
            if pole[y][x]==4:#шашка с короной
                for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                    true_move=0#определение правильности хода
                    for i in range(1,8):
                        if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                            if true_move==1:
                                spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                            if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or pole[y+iy*i][x+ix*i]==5:
                                true_move+=1
                            if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or pole[y+iy*i][x+ix*i]==6 or true_move==2:
                                if true_move>0:spisok.pop()#удаление хода из списка
                                break
            return spisok


        def check_hod_komp2(spisok):#проверка наличия остальных ходов
            for y in range(8):#сканируем всё поле
                for x in range(8):
                    if pole[y][x]==3 or pole[y][x]==6:#шашки
                        for ix,iy in (-1,1),(1,1):
                            if 0<=y+iy<=7 and 0<=x+ix<=7:
                                if pole[y+iy][x+ix]==0:
                                    spisok.append(((x,y),(x+ix,y+iy)))#запись хода в конец списка
                                if pole[y+iy][x+ix]==1 or pole[y+iy][x+ix]==2 or pole[y+iy][x+ix]==5:
                                    if 0<=y+iy*2<=7 and 0<=x+ix*2<=7:
                                        if pole[y+iy*2][x+ix*2]==0:
                                            spisok.append(((x,y),(x+ix*2,y+iy*2)))#запись хода в конец списка                  
                    if pole[y][x]==4:#шашка с короной
                        for ix,iy in (-1,-1),(-1,1),(1,-1),(1,1):
                            true_move=0#определение правильности хода
                            for i in range(1,8):
                                if 0<=y+iy*i<=7 and 0<=x+ix*i<=7:
                                    if pole[y+iy*i][x+ix*i]==0:
                                        spisok.append(((x,y),(x+ix*i,y+iy*i)))#запись хода в конец списка
                                    if pole[y+iy*i][x+ix*i]==1 or pole[y+iy*i][x+ix*i]==2 or pole[y+iy*i][x+ix*i]==5:
                                        true_move+=1
                                    if pole[y+iy*i][x+ix*i]==3 or pole[y+iy*i][x+ix*i]==4 or pole[y+iy*i][x+ix*i]==6 or true_move==2:
                                        break
            return spisok


        checkers_images()#загружаем шашки
        new_game()##начинаем новую партию игры
        draw_board(-1,-1,-1,-1)#рисуем шашечную доску
        doska.bind("<Motion>", position_one)
        doska.bind("<Button-1>", position_two)
        root.withdraw()
        main_window.protocol("WM_DELETE_WINDOW", root.destroy)
        mainloop()
           
    else:
        showerror("Ошибка", "Неверный логин или пароль.")

root = Tk() # Создаем окно
root.title("Регистрация или вход в игру Шашки царские башни") # Устанавливаем заголовок окна
root.geometry("400x300") # Устанавливаем размеры окна
root.configure(background="#F8F8FF")
font1 = font.Font(family="Verdana", size=11, weight="normal", slant="roman")
llogin = Label(font=font1, anchor=W, background="#F8F8FF", text="Введите Ваш логин")
llogin.pack(padx=6, pady=6)
login = Entry(bd=2)
login.pack(padx=6, pady=6)
lpassword = Label(font=font1, anchor=W, background="#F8F8FF", text="Введите Ваш пароль") 
lpassword.pack(padx=6, pady=6)
password = Entry(bd=2, show="*")
password.pack(padx=6, pady=6)
btn1 = Button(text="Войти", bg="#6b0568", fg="#FFFFFF", font=font1, command=enter_users)
btn1.pack(padx=6, pady=6) 
btn2 = Button(text="Зарегистрироваться", bg="#6b0568", fg="#FFFFFF", font=font1, command=registration_user)
btn2.pack(padx=6, pady=6) 

root.mainloop()