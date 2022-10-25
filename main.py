from tkinter import *
import tkinter
from time import sleep
from math import sin,cos,radians
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
def drawPolygon():
    global coords
    canvas.delete("all")
    print(coords)
    for i in range(len(coords)-1):
        BresenhamV4(coords[i][0],coords[i][1],coords[i+1][0] ,coords[i+1][1])

# сдвиг прямоугольника на n пикселей по горизонтали и y по вертикали
def shift(m,n):
    global counter,coords
    
    print('m = {} n = {}'.format(m,n))
    for i in range(len(coords)):
        coords[i][0] += m
        coords[i][1] += n
    drawPolygon()
      
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
    canvas.delete("all") 
    m,n = coords[0][0] , coords[0][1] # точка, относительно которой происходит сжатие расстяжение k > 1 растяг < 1 сжат.
    for i in range(len(coords)):
           coords[i][0] = round(coords[i][0]*k - m*k + m)
           coords[i][1] = round(coords[i][1]*k - n*k + n)
    drawPolygon()
def Turn(g):
    global counter,coords
    
    m,n = coords[len(coords)-1][0],coords[len(coords)-1][1]
    g = radians(g)
    for i in range(len(coords)-1):
           
           x1 = round(coords[i][0]*cos(g) - coords[i][1]*sin(g) - m*cos(g) + m + n*sin(g))
           y1 = round(coords[i][0] * sin(g) + coords[i][1]*cos(g) - m*sin(g) - n*cos(g) + n)
           x2 = round(coords[i+1][0]*cos(g) - coords[i+1][1]*sin(g) - m*cos(g) + m + n*sin(g))
           y2 = round(coords[i+1][0] * sin(g) + coords[i+1][1]*cos(g) - m*sin(g) - n*cos(g) + n)
           print([x1,y1,x2,y2]) 
           BresenhamV4(x1,y1,x2,y2) 
    pass        
#  Алгоритмы отрисовки ~

def rightBtn(event):
   global coords,counter
   # P.S сделать крутой выбор
   print('Coords: {}'.format(coords))
   Turn(30) 
    # сброс координат  
 #  coords = []
 #  counter = 0 
   pass
# ~ Смещения
def LShift(event):
    shift(-10,0)
    pass
def RShift(event):
    shift(10,0)
    pass
def UShift(event):
    shift(0,-10)
    pass
def DShift(event):
    shift(0,10)
#  Смещения ~


# ~  Скейлы
def ZoomIn(event):
    scale(1.1)
def ZoomOut(event):
    scale(0.9)
#  Скейлы ~ 



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
    global coords,counter
    coords = []
    counter = 0
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
    # Бинды клавиш
    canvas.bind("<Button-1>", callback)
    canvas.bind("<Button-3>", rightBtn)
    root.bind('<a>',LShift)
    root.bind('<d>',RShift)
    root.bind('<w>',UShift)
    root.bind('<s>',DShift)
    root.bind('<e>',ZoomIn )
    root.bind('<q>',ZoomOut)
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