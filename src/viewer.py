import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import Image, ImageTk

# 2 globals holding the canvas to draw on and the image data to draw
canvas = None
image_data = None

def get_file_format(file_path):
    return file_path.split('.')[-1].lower()


def handle_ppm(file_path):
    global image_data

    with open(file_path, 'r') as f:
        image_data = f.read()
    draw_plain_ppm()


def handle_png(file_path):
    global canvas

    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo


# Map file formats to handlers
format_handlers = {
    'ppm': handle_ppm,
    'png': handle_png
}

def main():
    global canvas
    window = tk.Tk()
    window.geometry("600x600")
    ttk.Button(window,text="open",command=draw_image).pack()
    canvas = tk.Canvas(window,width=500,height=500,background="white")
    canvas.pack()
    window.mainloop()



#currently treats file as text, not binary data
def draw_image():
    # for now only opens in text mode, doesnt return stream of bytes
    global image_data
    file = fd.askopenfile()
    image_data = file.read()
    if "P3" in image_data:
        draw_plain_ppm()




def dec_to_hex(dec):
    n1 = 15&dec
    n2 = (240&dec)//16 #shifts left by 4
    hex_string = ""
    if n1 > 9:
        hex_string+=chr(55+n1) #55 is A-10 in ascii
    else:
        hex_string+=chr(n1+48)
    if n2 > 9:
        hex_string+=chr(55+n2) #55 is A-10 in ascii
    else:
        hex_string+=chr(n2+48)

    return hex_string

#returns string since file is opened as text file, later should also return bytes for binary data
def draw_plain_ppm():
    #plain ppm files are just text
    global image_data
    global canvas
    data = image_data.split()
    width = data[1]
    height = data[2]
    value_range = data[3]
    
    index = 4
    col  = 0
    row = 0
    pixel_width = 10
    pixel_height = 10
    print(len(data))
    while index < len(data):
        #incredibly stupid
        if(col == 4):
            col = 0
            row+=1
        r = dec_to_hex(int(data[index]))
        g = dec_to_hex(int(data[index+1]))
        b = dec_to_hex(int(data[index+2]))
        canvas.create_rectangle(col*pixel_width,row*pixel_height,col*pixel_width+pixel_width,row*pixel_height+pixel_height,fill=(f"#{r}{g}{b}"))
        index+=3
        col+=1

main()
