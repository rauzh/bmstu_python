'''
Rauzhev Pavel, IU7-23B
The program realizes steganography encoing & decoding text with PNG image.
'''

from tkinter import *
import tkinter.messagebox as box

from PIL import Image, ImageDraw
from tkinter import filedialog as fd

# ------------------------DEFAULT------------------------------------------------------------------------
color_bg = "thistle1"
color_but = "MediumPurple3"
color_but_text = "lavender"
fnt = 'Arial'

# ------------------------WINDOW-------------------------------------------------------------------------
window = Tk()
window['bg'] = color_bg
window.title('3nc0d3r_1700')
window.geometry(f'528x488+100+200')
window.resizable(width=False, height=False)

# -----------------------ENTRY--------------------------------------------------------------------------
# Text to encode entry
enc_text = Label(window, text='Input message:', bg=color_bg, font=fnt + ' 16')
enc_text.grid(row=0, column=0, pady=5, sticky=W, padx=5)
enc_input = Entry(window, font=fnt + ' 12', bd=30)
enc_input.grid(row=1, column=0, sticky=W + E, pady=5, padx=10, columnspan=2)

space_1 = Label(window, text='                                          ', bg=color_bg, font=fnt + ' 16')
space_1.grid(row=0, column=1, pady=5, sticky=W + E)

# Name of pic entry
pic_text = Label(window, text='Encoded image name:       ', bg=color_bg, font=fnt + ' 16')
pic_text.grid(row=2, column=0, pady=5, sticky=W, padx=5)
pic_input = Entry(window, font=fnt + ' 12', bd=30)
pic_input.grid(row=2, column=1, sticky=W + E, pady=5, padx=10)


# Output entry
dec_text = Label(window, text='Output message: ', bg=color_bg, font=fnt+' 16')
dec_text.grid(row=4, column=0, pady=5, sticky=W, padx=10)
dec_input = Entry(window, font=fnt+' 12', bd=30)
dec_input.config(state="readonly")
dec_input.grid(row=5, column=0, sticky=W+E, pady=5, padx=10, columnspan=2)

space_2 = Label(window, text='                                          ', bg=color_bg, font=fnt+' 16')
space_2.grid(row=4, column=1, pady=5, sticky=W+E)


# ------------------------COMMANDS-----------------------------------------------------------------------


# ------------------------BUTTONS-------------------------------------------------------------------------
# Encode button
Button(window, text='Encode message', width=6, height=2, bg=color_but, command=lambda: encode_msg(),
       font=('Arial 16'), fg=color_but_text, bd=30).grid(row=3, column=0, stick=N + S + W + E, padx=10, pady=5)
Button(window, text='Decode message', width=6, height=2, bg=color_but, command=lambda: decode_msg(),
       font=('Arial 16'), fg=color_but_text, bd=30).grid(row=3, column=1, stick=N + S + W + E, padx=10, pady=5)


# ------------------------MENU---------------------------------------------------------------------------
mainmenu = Menu(window)
window.config(menu=mainmenu)

mainmenu.add_command(label="Info", command=lambda: info_msg())

# ------------------------MESSAGE------------------------------------------------------------------------
def info_msg():
    box.showinfo('Some info',
                 "The program's intended to find roots of functions using half-interval method.\n"
                 "Born & Raised by Pavel Rauzhev")


# ------------------------PROCESSING---------------------------------------------------------------------

# Перевод символа в двоичный вид по кодировке
def get_num_bin(char):
    num_int = char.encode("windows-1251")
    num_bin = bin(num_int[0])[2:]
    num_bin = (8 - len(num_bin)) * "0" + num_bin
    return num_bin

# Перевод строки в двоичный вид
def msg_to_bin(msg):
    bin_msg = ""
    for char in msg:
        num_bin = get_num_bin(char)
        bin_msg += num_bin
    return bin_msg

# Получение символа из байта по кодировке
def get_char_from_bin(num_bin):
    num_int = int(num_bin, 2)
    num_byte = num_int.to_bytes(1, byteorder="big")
    char = num_byte.decode("windows-1251")
    return char


def change_last_bit(width, height, pix, bin_msg, draw):
    count_channels = len(pix[0, 0])
    index = 0
    for x in range(width):
        for y in range(height):
            for z in range(count_channels):

                if index == len(bin_msg):
                    return pix

                bit = int(bin_msg[index])
                channel = pix[x, y][z]

                if (bit == 0b0):
                    channel &= ~0b1
                else:
                    channel |= 0b1

                channels = list(pix[x, y])
                channels[z] = channel
                channels = tuple(channels)

                draw.point((x, y), channels)
                index += 1


def decode_img(width, height, pix):
    string = ""
    byte = ""
    count_channels = len(pix[0, 0])
    count_bits = 0
    for x in range(width):
        for y in range(height):
            for z in range(count_channels):

                if (count_bits == 8):

                    char = get_char_from_bin(byte)
                    if (char == "$"):
                        return string

                    string += char
                    count_bits = 0
                    byte = ""

                channel = pix[x, y][z]

                bit = channel & 0b1

                byte += str(bit)
                count_bits += 1


def encode_msg():
    filetypes = (('image files', '*.PNG'),)

    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    msg = enc_input.get()
    end_point = "$"
    msg = msg + end_point
    bin_msg = msg_to_bin(msg)
    pix = change_last_bit(width, height, pix, bin_msg, draw)

    box.showinfo("Report", "Image encoded successfully. Choose path to save the image")

    folder = fd.askdirectory()
    name = "/" + pic_input.get()
    if name[-4:] != ".png":
        name += ".png"
    image.save(folder + name, "PNG")

    box.showinfo("Report", "Image saved successfully.")


def decode_msg():
    filetypes = (('image files', '*.PNG'),)

    box.showinfo("Report", "Choose .png image to decode")
    filename = fd.askopenfilename(title='Open a file', initialdir='/', filetypes=filetypes)
    name = filename.split("/")[-1]
    image = Image.open(filename)
    draw = ImageDraw.Draw(image)
    width = image.size[0]
    height = image.size[1]
    pix = image.load()

    string = decode_img(width, height, pix)
    box.showinfo("Report", "Message decoded successfully")
    dec_input.config(state="normal")
    dec_input.delete(0, END)
    dec_input.insert(0, string)
    dec_input.config(state="readonly")

# ------------------------
window.mainloop()
