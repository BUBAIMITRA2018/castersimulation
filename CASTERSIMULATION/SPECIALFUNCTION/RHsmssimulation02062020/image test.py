import tkinter
from tkinter import *
from PIL import Image, ImageTk

root = Tk()

make_frame = LabelFrame(root, text="Sample Image", width=100, height=100)
make_frame.pack()

stim_filename = "smslogo.png"

# create the PIL image object:
PIL_image = Image.open(stim_filename)

width = 100
height = 100

# You may prefer to use Image.thumbnail instead
# Set use_resize to False to use Image.thumbnail
use_resize = True

if use_resize:
    # Image.resize returns a new PIL.Image of the specified size
    PIL_image_small = PIL_image.resize((width,height), Image.ANTIALIAS)
else:
    # Image.thumbnail converts the image to a thumbnail, in place
    PIL_image_small = PIL_image
    PIL_image_small.thumbnail((width,height), Image.ANTIALIAS)

# now create the ImageTk PhotoImage:
img = ImageTk.PhotoImage(PIL_image_small)
in_frame = Label(make_frame, image = img)
in_frame.pack()

root.mainloop()