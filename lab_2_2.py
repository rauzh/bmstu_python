'''
Rauzhev Pavel, IU7-23B

'''

from tkinter import *
import tkinter.messagebox as box

from math import  *
import numpy as np

import pygame

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# ------------------------DEFAULT------------------------------------------------------------------------
color_bg = "thistle1"
color_but = "MediumPurple3"
color_but_text = "lavender"
fnt = 'Arial'

# ------------------------WINDOW-------------------------------------------------------------------------
window = Tk()
window['bg'] = color_bg
window.title('LAB_2')
window.geometry(f'1020x350+100+200')
window.resizable(width=False, height=False)

# -----------------------ENTRY--------------------------------------------------------------------------
# f(x) entry
func_input_text = Label(window, text='f(x):', bg=color_bg, font=fnt+' 40')
func_input_text.grid(row=0, column=0, pady=5)
func_input = Entry(window, font=fnt+' 20', bd=30)
func_input.grid(row=0, column=1, sticky=W+E, pady=5, padx=10, columnspan=4)

# a entry
a_input_text = Label(window, text='a:', bg=color_bg, font=fnt)
a_input_text.grid(row=1, column=0, pady=2)
a_input = Entry(window, font=fnt)
a_input.grid(row=2, column=0, sticky=W+E, pady=2, padx=10)

# b entry
b_input_text = Label(window, text='b:', bg=color_bg, font=fnt)
b_input_text.grid(row=1, column=1, pady=2)
b_input = Entry(window, font=fnt)
b_input.grid(row=2, column=1, sticky=W+E, pady=2, padx=10)

# h entry
h_input_text = Label(window, text='h:', bg=color_bg, font=fnt)
h_input_text.grid(row=1, column=2, pady=2)
h_input = Entry(window, font=fnt)
h_input.grid(row=2, column=2, sticky=W+E, pady=2, padx=10)

# Nmax entry
n_max_input_text = Label(window, text='Nmax:', bg=color_bg, font=fnt)
n_max_input_text.grid(row=1, column=3, pady=2)
n_max_input = Entry(window, font=fnt)
n_max_input.grid(row=2, column=3, sticky=W+E, pady=2, padx=10)

# eps entry
eps_input_text = Label(window, text='eps:', bg=color_bg, font=fnt)
eps_input_text.grid(row=1, column=4, pady=2)
eps_input = Entry(window, font=fnt)
eps_input.grid(row=2, column=4, sticky=W+E, pady=2, padx=10)

# -----------------------CORE---------------------------------------------------------------------------
# f(x)
def f(x):
    try:
        return eval(func_input.get())
    except: return 'FAIL'

# Break on sections
def find_intervals(a, b, h, eps):
    x_0 = a
    arr = []

    while 1:
        if f(x_0) == 'FAIL' and x_0 <= b - h:
            x_0 += h
        else: break

    if abs(x_0) < h: x_0 = 0.0

    x_1 = x_0 + h

    if f(x_1) == 'FAIL': return arr

    while (x_1 <= b):
        if abs(f(x_0)) < eps:
            arr.append((x_0, x_1))
        elif abs(f(x_1)) < eps:
            arr.append((x_0, x_1))
        elif f(x_0) * f(x_1) < 0:
            arr.append((x_0, x_1))
        x_0 += h
        x_1 += h
        if abs(x_0) < eps and x_0 < 0: x_0 = 0 - eps
        if abs(x_1) < eps and x_1 > 0: x_1 = 0 + eps
        if abs(x_1) < eps and x_1 < 0: x_1 = 0 - eps
        if abs(x_0) < eps and x_0 > 0: x_0 = 0 + eps
    return arr


# Get results
def half_int_method(a, b, eps, n_max, j):
    section = "[{:<9.4}; {:>9.4}]".format(a, b)
    y1 = f(a)
    y2 = f(b)
    if y1 == 'FAIL' or y2 == 'FAIL': return [j + 1, section, "Error", "Error", "Error", 3]
    if abs(y1) < eps: return [j + 1, section, format(a, "<9.4"), format(y1, "<7.5"), 0, 0]
    if abs(y2) < eps: return [j + 1, section, format(b, "<9.4"), format(y2, "<7.5"), 0, 0]
    if y1 * y2 >= abs(eps): return [j + 1, section, "Error", "Error", "Error", 2]
    for i in range(n_max + 1):
        x = (a + b) / 2
        y3 = f(x)
        if y3 == 'FAIL': return [j + 1, section, "Error", "Error", "Error", 3]
        if y1 * y3 < 0:
            b = x
        else:
            a = x
        if (abs(y3)) < eps:
            break
    else:
        return j + 1, section, "Error", "Error", "Error", 1
    return [j + 1, section, format(x, "<9.4"), format(y3, "<7.5"), i + 1, 0]
    #return [j + 1, [a, b], format(x, "<9.4"), format(y3, "<7.5"), i + 1, 0]

def lessgoo():
    try:
        a = float(a_input.get())
        b = float(b_input.get())
        h = abs(float(h_input.get()))
        n_max = int(n_max_input.get())
        eps = float(eps_input.get())
        intervals = find_intervals(a, b, h, eps)
        print(intervals)
        table_arr = []
        for i in range(len(intervals)):
            table_arr.append(half_int_method(intervals[i][0], intervals[i][1], eps, n_max, i))
            print(*table_arr[i])

        if table_arr:
            for wow in range(len(table_arr) // 23):
                table(table_arr, wow*23, wow*23 + 23)
            table(table_arr, (len(table_arr) // 23) * 23, len(table_arr))
        if f(a) == 'FAIL' and f(b) != 'FAIL':
            plot(intervals[0][0], b)
        elif f(a) != 'FAIL' and f(b) == 'FAIL':
            plot(a, intervals[-1][1])
        elif f(a) != 'FAIL' and f(b) != 'FAIL':
            plot(a, b)
        elif intervals:
            plot(intervals[0][0], intervals[-1][1])
    except: oops_msg()
# -----------------------TABLE--------------------------------------------------------------------------

def table(tab_data, start, end):
    tab = Toplevel(window)
    tab.title('TABLE OF RESULTS')
    tab.resizable(width=False, height=False)
    tab.geometry(f'900x640+100+200')
    tab['bg'] = color_bg

    Label(tab, text="_" * 100,
          bg=color_bg, font=fnt).grid(row=0, columnspan=12)

    Label(tab, text="root №",
          bg=color_bg, font=fnt, width=10).grid(row=1, column=0, stick=W + E)
    Label(tab, text=" | ",
          bg=color_bg, font=fnt, width=3).grid(row=1, column=1, stick=E + W)
    Label(tab, text="[x_i ; x_i+1]",
          bg=color_bg, font=fnt, width=15).grid(row=1, column=2, stick=E + W)
    Label(tab, text=" | ",
          bg=color_bg, font=fnt, width=3).grid(row=1, column=3, stick=E + W)
    Label(tab, text="x'",
          bg=color_bg, font=fnt, width=10).grid(row=1, column=4, stick=E + W)
    Label(tab, text=" | ",
          bg=color_bg, font=fnt, width=3).grid(row=1, column=5, stick=E + W)
    Label(tab, text="f(x')",
          bg=color_bg, font=fnt, width=10).grid(row=1, column=6, stick=E + W)
    Label(tab, text=" | ",
          bg=color_bg, font=fnt, width=3).grid(row=1, column=7, stick=E + W)
    Label(tab, text="Num of iters",
          bg=color_bg, font=fnt, width=10).grid(row=1, column=8, stick=E + W)
    Label(tab, text=" | ",
          bg=color_bg, font=fnt, width=3).grid(row=1, column=9, stick=E + W)
    Label(tab, text="Error code",
          bg=color_bg, font=fnt, width=10).grid(row=1, column=10, stick=E + W)
    Label(tab, text=" | ",
          bg=color_bg, font=fnt, width=3).grid(row=1, column=11, stick=E + W + S)

    Label(tab, text="~" * 100,
          bg=color_bg, font=fnt).grid(row=2, columnspan=12)

    for i in range(start, end):
        Label(tab, text=str(tab_data[i][0]),
              bg=color_bg, font=fnt, width=10).grid(row=i + 3, column=0, stick=E + W)
        Label(tab, text=" | ",
              bg=color_bg, font=fnt, width=3).grid(row=i + 3, column=1, stick=E + W)
        Label(tab, text=str(tab_data[i][1]),
              bg=color_bg, font=fnt, width=15).grid(row=i + 3, column=2, stick=E + W)
        Label(tab, text=" | ",
              bg=color_bg, font=fnt, width=3).grid(row=i + 3, column=3, stick=E + W)
        Label(tab, text=str(tab_data[i][2]),
              bg=color_bg, font=fnt, width=10).grid(row=i + 3, column=4, stick=E + W)
        Label(tab, text=" | ",
              bg=color_bg, font=fnt, width=3).grid(row=i + 3, column=5, stick=E + W)
        Label(tab, text=str(tab_data[i][3]),
              bg=color_bg, font=fnt, width=10).grid(row=i + 3, column=6, stick=E + W)
        Label(tab, text=" | ",
              bg=color_bg, font=fnt, width=3).grid(row=i + 3, column=7, stick=E + W)
        Label(tab, text=str(tab_data[i][4]),
              bg=color_bg, font=fnt, width=10).grid(row=i + 3, column=8, stick=E + W)
        Label(tab, text=" | ",
              bg=color_bg, font=fnt, width=3).grid(row=i + 3, column=9, stick=E + W)
        Label(tab, text=str(tab_data[i][5]),
              bg=color_bg, font=fnt, width=10).grid(row=i + 3, column=10, stick=E + W)
        Label(tab, text=" | ",
              bg=color_bg, font=fnt, width=3).grid(row=i + 3, column=11, stick=E + W)



# -----------------------MATPLOTLIB---------------------------------------------------------------------
def plot(a, b):
    fig = Figure(figsize=(5, 5))
    subplot = fig.add_subplot()
    X_mn = np.linspace(a, b, int((b - a) * 1000))

    Y_mn = [f(i) for i in X_mn]
    Y_mn = np.array(Y_mn)
    diff_1 = np.diff(Y_mn)
    diff_2 = np.diff(diff_1)

    mask = np.abs(Y_mn) < 1e-5
    mask_1 = np.abs(diff_1) < 1e-5
    mask_2 = np.abs(diff_2) < 1e-8
    subplot.plot(X_mn, Y_mn)
    subplot.scatter(X_mn[mask], Y_mn[mask], color='purple', s=40, marker='o', label='zeros')
    subplot.scatter(X_mn[:-1][mask_1], Y_mn[:-1][mask_1], color='green', s=40, marker='o', label='extreme points')
    subplot.scatter(X_mn[:-2][mask_2], Y_mn[:-2][mask_2], color='red', s=40, marker='o', label='inflection points')

    subplot.grid()

    plotik = Toplevel(window)
    plotik.title('f(x) GRAPHIC')
    plotik.resizable(width=False, height=False)
    plotik.geometry(f'545x545+100+200')
    plotik['bg'] = color_bg

    canvas = FigureCanvasTkAgg(fig, plotik)
    canvas.draw()
    canvas.get_tk_widget().grid(row=6, column=0, rowspan=3, columnspan=6, stick='wens', padx=20, pady=20)


# -----------------------BUTTONS------------------------------------------------------------------------

Button(window, text='GET RESULT', width=6, command=lambda: lessgoo(), height=2, bg=color_but, font=('Arial 30'),
       fg=color_but_text, bd=30).grid(row=3, columnspan=5, stick=N+S+W+E, padx=5, pady=5)

# ------------------------MESSAGE------------------------------------------------------------------------
def info_msg():
    box.showinfo('Some info',
                 "The program's intended to find roots of functions using half-interval method.\n"
                 "Born & Raised by Pavel Rauzhev")

def code_msg():
    box.showinfo('Error codes',
                 "0 - root's found successfully\n"
                 "1 - too many iterations\n"
                 "2 - no root in the interval\n"
                 "3 - function is undefined in this interval")

def oops_msg():
    box.showinfo('OOPS!',
                 "OHH NOOOO INCORRECT INPUT!!!")

# ------------------------MENU---------------------------------------------------------------------------
mainmenu = Menu(window)
window.config(menu=mainmenu)

mainmenu.add_command(label="Info", command=lambda: info_msg())

mainmenu.add_command(label="Error codes", command=lambda: code_msg())

# -----------------------STUFF--------------------------------------------------------------------------

pygame.mixer.init()
pygame.mixer.music.load("8bit.mp3")
pygame.mixer.music.play()

window.mainloop()
