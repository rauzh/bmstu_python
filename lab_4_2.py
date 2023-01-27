'''
Rauzhev Pavel, IU7-23B
The program realizes steganography encoing & decoding text with PNG image.
'''

from tkinter import *
import tkinter.messagebox as box

# ------------------------DEFAULT------------------------------------------------------------------------
color_bg = "thistle1"
color_but = "MediumPurple3"
color_but_text = "lavender"
fnt = 'Arial'
canvas_width = 242
canvas_height = 256
handed_width = 256

# ------------------------WINDOW-------------------------------------------------------------------------
window = Tk()
window['bg'] = color_bg
window.title('C0nV3x_f1nd3R 228')
window.geometry(f'525x620+100+200')
window.resizable(width=False, height=False)


# -----------------------DEFS---------------------------------------------------------------------------

def click(event):
    if not ((event.x, event.y) in points):
        check_result()
        draw(event.x, event.y)
        points.append((event.x, event.y))


# -----------------------ENTRY--------------------------------------------------------------------------
x_text = Label(window, text='X:', bg=color_bg, font=fnt + ' 16')
x_text.grid(row=0, column=0, pady=5, sticky=W + E, padx=5)

x_input = Entry(window, font=fnt + ' 12', bd=30)
x_input.grid(row=1, column=0, sticky=W + E, pady=5, padx=10)

y_text = Label(window, text='Y:', bg=color_bg, font=fnt + ' 16')
y_text.grid(row=0, column=1, pady=5, sticky=W + E, padx=5)

y_input = Entry(window, font=fnt + ' 12', bd=30)
y_input.grid(row=1, column=1, sticky=W + E, pady=5, padx=10)

ip_text = Label(window, text='Pick points:', bg=color_bg, font=fnt + ' 16')
ip_text.grid(row=3, column=0, pady=5, sticky=W + E, padx=5)

space_2 = Label(window, text='', bg=color_bg, font=fnt + ' 16').grid(row=4, column=0,
                                                                     sticky=W + E + S + N, pady=5, padx=10, )
space_3 = Label(window, text='', bg=color_bg, font=fnt + ' 16').grid(row=5, column=0,
                                                                     sticky=W + E + S + N, pady=5, padx=10, )
space_4 = Label(window, text='', bg=color_bg, font=fnt + ' 16').grid(row=6, column=0,
                                                                     sticky=W + E + S + N, pady=5, padx=10, )
space_5 = Label(window, text='', bg=color_bg, font=fnt + ' 16').grid(row=7, column=0,
                                                                     sticky=W + E + S + N, pady=5, padx=10, )

can_frame = Frame(window, width=canvas_width, height=canvas_height)
can_frame.pack_propagate(False)
can_frame.place(x=10, y=240)

canvas = Canvas(can_frame, bg=color_but_text)
canvas.pack(fill=BOTH, expand=True)
canvas.bind("<1>", click)

num_text = Label(window, text='Num of rectangles:', bg=color_bg, font=fnt + ' 16')
num_text.grid(row=3, column=1, sticky=W + E + S + N, pady=5, padx=10)

num = Label(window, text='0', bg=color_bg, font=fnt + ' 48')
num.grid(row=4, column=1, sticky=W + E + S + N, pady=5, padx=10, rowspan=3)


# ------------------------COMMANDS-----------------------------------------------------------------------
def canvas_clear():
    canvas.delete("all")
    clean_result()
    points.clear()
    box.showinfo("Canvas", "Canvas is cleared")


def clean_result():
    result.clear()
    num["text"] = ''


def show_all():
    if not result:
        return
    for i in result:
        show_result(i, False)


def calculate():
    calculate_result()


# ------------------------BUTTONS-------------------------------------------------------------------------

Button(window, text='Add point', width=6, height=1, bg=color_but, command=lambda: add_point(),
       font=('Arial 16'), fg=color_but_text, bd=30).grid(row=2, column=0, stick=N + S + W + E,
                                                         padx=10, pady=5, columnspan=2)

Button(window, text='Clear canvas', width=6, height=1, bg=color_but, command=lambda: canvas_clear(),
       font=('Arial 16'), fg=color_but_text, bd=30).grid(row=10, column=0, stick=N + S + W + E,
                                                         padx=10, pady=5)

Button(window, text='Show result', width=6, height=1, bg=color_but, command=lambda: show_all(),
       font=('Arial 16'), fg=color_but_text, bd=30).grid(row=10, column=1, stick=N + S + W + E,
                                                         padx=10, pady=5)

Button(window, text='Calculate', width=6, height=1, bg=color_but, command=lambda: calculate(),
       font=('Arial 16'), fg=color_but_text, bd=30).grid(row=7, column=1, stick=N + S + W + E,
                                                         padx=10, pady=5)
# ------------------------MENU---------------------------------------------------------------------------
mainmenu = Menu(window)
window.config(menu=mainmenu)

mainmenu.add_command(label="Info", command=lambda: info_msg())


# ------------------------MESSAGE------------------------------------------------------------------------
def info_msg():
    box.showinfo('Some info',
                 "The program's intended to find num of convex quadrilaterals on canvas by points.\n"
                 "Born & Raised by Pavel Rauzhev")


# ------------------------PROCESSING---------------------------------------------------------------------
points = []
result = []

def draw(x, y):
    canvas.create_oval(x, y, x, y, fill="Black")


def redraw_values():
    canvas.delete("all")
    for i in points:
        draw(i[0], i[1])


def check_result():
    if result:
        clean_result()
        redraw_values()
        box.showinfo("Results", "Data changes, results reset")


def add_point():
    x = x_input.get()
    y = y_input.get()

    try:
        x = float(x)
        if x < 1 or x > canvas_width - 2:
            box.showerror("Invalid х", "Out of canvas limits")
            return
    except:
        box.showerror("Invalid х", "Incorrect input")
        return

    try:
        y = float(y)
        if y < 1 or y > canvas_height - 2:
            box.showerror("Invalid y", "Out of canvas limits")
            return
    except:
        box.showerror("Invalid y", "Incorrect input")
        return

    if not ((x, y) in points):
        check_result()
        draw(x, y)
        points.append((x, y))
        x_input.delete(0, END)
        y_input.delete(0, END)
    else:
        box.showerror("Value", "This point already exists")
        return


def get_sign(value):
    try:
        return value / abs(value)
    except:
        return 0

'''
точки а б с д
смотрим расстояния между ними по иксу и игрику
если совпадают точки то континью

потом такие ееее формула взятая с какого-то форума по си 2005 года
(диагонали, проверяем внутри ли они фигуры)

если всё хорошо, то закидываем кортеж из четырёх точек в массив

заполняет список четвёрками точек, образующих выпуклые четырёхугольники
'''
def calculate_result():
    enumerated_points = list(enumerate(points))
    for i, a in enumerated_points:
        for j, b in enumerated_points:
            if j == i:
                continue
            d_ab = (b[0] - a[0], b[1] - a[1])
            for k, c in enumerated_points:
                if k == j or k == i:
                    continue
                d_ac = (c[0] - a[0], c[1] - a[1])
                d_bc = (c[0] - b[0], c[1] - b[1])
                for l, d in enumerated_points:
                    if l == k or l == j or l == i:
                        continue
                    d_ad = (d[0] - a[0], d[1] - a[1])
                    d_bd = (d[0] - b[0], d[1] - b[1])
                    d_cd = (d[0] - c[0], d[1] - c[1])

                    ad_pos = [get_sign(d_ad[0] * d_ab[1] - d_ad[1] * d_ab[0]),
                              get_sign(d_ad[0] * d_ac[1] - d_ad[1] * d_ac[0])]
                    ab_pos = [get_sign(d_ab[0] * d_ac[1] - d_ab[1] * d_ac[0]),
                              get_sign(d_ab[0] * d_ad[1] - d_ab[1] * d_ad[0])]
                    bc_pos = [- get_sign(d_bc[0] * d_ab[1] + d_bc[1] * d_ab[0]),
                              get_sign(d_bc[0] * d_bd[1] - d_bc[1] * d_bd[0])]
                    cd_pos = [get_sign(d_cd[0] * d_ac[1] - d_cd[1] * d_ac[0]),
                              get_sign(d_cd[0] * d_bc[1] - d_cd[1] * d_bc[0])]

                    if ad_pos[0] == ad_pos[1] and ab_pos[0] == ab_pos[1]\
                            and bc_pos[0] == bc_pos[1] and cd_pos[0] == cd_pos[1]:
                        res = (i, j, k, l)
                        s_res = tuple(sorted(res))
                        for r in result:
                            if s_res == tuple(sorted(r)):
                                break
                        else:
                            result.append((i, j, k, l))
    if len(result):
        box.showinfo("Results", "{:1} convex rectangles found".format(len(result)))
        num["text"] = str(len(result))
    else:
        box.showerror("Results", "No convex rectangles found")


def show_result(result, clear=True):
    if clear:
        redraw_values()
    canvas.create_line(*points[result[0]], *points[result[1]])
    canvas.create_line(*points[result[1]], *points[result[2]])
    canvas.create_line(*points[result[2]], *points[result[3]])
    canvas.create_line(*points[result[3]], *points[result[0]])


# ------------------------

window.mainloop()
