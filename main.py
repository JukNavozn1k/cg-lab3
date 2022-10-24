from tkinter import *
import tkinter
from time import sleep

# ~ Необходимые переменные
# Необходимые переменные ~ 
 
# ~ Дополнительные методы
def sign(x):
    if x >= 0: return 1
    return -1
# Дополнительные методы ~

# ~ Алгоритмы отрисовки
def draw_dot(x,y,col='black'):
    global root,sbsm
    x1,y1 = x-1,y-1
    x2,y2 = x+1,y+1
    if sbsm.get() == 0:canvas.create_oval(x1, y1, x2, y2,fill=col,width=1,outline=col) 
    else:
        sleep(0.001)
        canvas.create_oval(x1, y1, x2, y2,fill='red',width=1,outline='red') 
        root.update()

def BresenhamV4(x1,y1,x2,y2): # четырёхсвязная развёртка 
    x,y,dx,dy,s1,s2 = x1,y1,abs(x2-x1),abs(y2-y1),sign(x2-x1),sign(y2-y1)
    l = None
    if dy<dx: l = False
    else:
        l = True
        dx,dy = dy,dx
    e = 2*dy-dx
    for i in range(1,dx+dy):
        draw_dot(x,y)
        if e < 0:
            if l: y = y + s2
            else: x = x + s1
            e = e+2*dy
        else:
            if l : x = x + s1
            else: y = y + s2
            e = e - 2*dx
    draw_dot(x,y)
# сдвиг прямоугольника на n пикселей по горизонтали и y по вертикали
def shift(x,y):
    global counter,coords
    m , n = x - coords[len(coords)-1][0] , y - coords[len(coords)-1][1]
    print('m = {} n = {}'.format(m,n))
    for i in range(len(coords)-1):
        BresenhamV4(m+coords[i][0],n+coords[i][1],m+coords[i+1][0],n+coords[i+1][1]) 
# Отражение относительно оси X
def mirrorX():
    global counter,coords
   
    for i in range(len(coords)-1):
        BresenhamV4(canvas.winfo_width()- coords[i][0], coords[i][1],canvas.winfo_width() -coords[i+1][0], coords[i+1][1]) 
 # Отражение относительно оси Y  
def mirrorY():
    global counter,coords
   
    for i in range(len(coords)-1):
        BresenhamV4(coords[i][0], canvas.winfo_height()-coords[i][1],coords[i+1][0], canvas.winfo_height()- coords[i+1][1]) 
def scale(k=1):
    
    m,n = coords[0][0] , coords[0][1] # точка, относительно которой происходит сжатие расстяжение k > 1 растяг < 1 сжат.
    for i in range(len(coords)-1):
           BresenhamV4(round(coords[i][0]*k - m*k + m), round(coords[i][1]*k - n*k + n), round(coords[i + 1][0]*k - m*k + m), round(coords[i + 1 ][1]*k - n*k + n)) 
        
#  Алгоритмы отрисовки ~

def rightBtn(event):
   global coords,counter
   # P.S сделать крутой выбор
   print('Coords: {}'.format(coords))
   mirrorX() 
    # сброс координат  
   coords = []
   counter = 0 
   pass

# ~UI Функционал
def callback(event): # метод отслеживания нажатий
    global counter,coords,var
    coords.append([int(event.x),int(event.y)])
    if len(coords) > 1:
        tmp = len(coords)
        BresenhamV4(coords[tmp-2][0],coords[tmp-2][1],coords[tmp-1][0],coords[tmp-1][1])
         
    print('Current click: ',counter + 1)
    counter += 1

def clear(): # очистить холст
    canvas.delete("all") 
# UI Функционал~

if __name__ == "__main__":
    # Инициализация и базовая настройки окна
    root = Tk()
    root.title('Лабораторная работа № 3 Аффинные преобразования на плоскости')
    root.resizable(0, 0)

    # Инициализация важных переменных
    counter = 0 # переменная, в которой хранится номер клика мыши
    coords = [] # координаты точек
    
    
    # Инициализация и настройка холста
    canvas= Canvas(root, width=800, height=600,bg='white')
    canvas.bind("<Button-1>", callback)
    canvas.bind("<Button-3>", rightBtn)
    canvas.pack()
    # Step by step mode (animation)
    sbsm = IntVar()
    sbsmCBtn = Checkbutton(root, text = "Step by step mode",
                      variable = sbsm,
                      onvalue = 1,
                      offvalue = 0)
    sbsmCBtn.pack()
    # Вспомогательные многоугольники
   

    # Кнопка очистки очистка холста
    clsBtn = tkinter.Button(root,text='Очистить холст',command=clear)
    clsBtn.pack()
    root.mainloop()