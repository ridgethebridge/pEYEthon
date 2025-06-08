import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from PIL import Image, ImageTk

#globals holding the window and its stuff
canvas = None
image_data = None
window = None

def get_file_format(file_path):
    return file_path.split('.')[-1].lower()

#handles pgm, jpeg, png, gif, and ppm by default, it can just be on function for those formats
def handle_image(file_path):
    global canvas
    image = Image.open(file_path)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=photo)
    canvas.image = photo

# Map file formats to handlers
format_handlers = {
    'ppm': handle_image,
    'png': handle_image,
    'jpg': handle_image,
    'gif': handle_image
}

def main():
    global canvas
    global window
    window = tk.Tk()
    window.geometry("600x600")
    window.option_add("*tearOff",tk.FALSE) #disallows menu tearoff
    menubar = tk.Menu(window)
    window["menu"] = menubar
    canvas = tk.Canvas(window,width=500,height=500,background="white")
    canvas.pack()
    window.update_idletasks() #idk but necessary to get proper width
    menu_file = tk.Menu(menubar)
    menu_edit = tk.Menu(menubar)
    menubar.add_cascade(menu=menu_file,label="File")
    menubar.add_cascade(menu=menu_edit,label="Edit")
    menu_file.add_command(label="Open",command = draw_image)
    menu_edit.add_command(label="Crop",command=crop_image)
    window.mainloop()


#currently treats file as text, not binary data
def draw_image():
    # Create list of supported file formts
    filetypes = [("Image files", " " + " ".join([f"*.{ext}" for ext in format_handlers.keys()]))]
    # Only opens supported file formats
    file_path = fd.askopenfilename(filetypes=filetypes)

    if not file_path:
        return

    # Get the file format
    file_format = get_file_format(file_path)

    # Use format handler from map for file format
    if file_format in format_handlers:
        format_handlers[file_format](file_path)
    else:
        print("File format not supported")


#not implemented yet
def crop_image():
    pass


main()
