from tkinter import *
from PIL import ImageTk, Image
import settings

root = Tk()

class QuantumGui():

    def __init__(self):
        self.currentSet = 1
        self.images = [] # [0] = big image // [1] to [3] = smaller images

        self.frame = Frame(root, width=1280, height=720)
        self.frame.grid(row=0, column=0, sticky="nsew")

        root.minsize(600,600)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)

        self.initLabels()
        self.update()
        mainloop()
    
    def initLabels(self):
        width = int(settings.windowBaseWidth / 2)
        height = int(settings.windowBaseWidth / 2)

        img = resize(Image.open("test2.png"), width, height, Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(img)
        l = Label(self.frame, image=photo)
        l.image = photo
        l.grid(row=1, column=0, rowspan=1)
        self.images.append(l)
        for i in range(settings.snapsPerSet):
            # Smaller images
            img = resize(Image.open("snap_{},{}.tif".format(
                self.currentSet, i+1)).convert("RGB"), width, int(height/3), Image.ANTIALIAS)
            photo = ImageTk.PhotoImage(img)
            l = Label(self.frame, image=photo)
            l.image = photo
            l.grid(row=i, column=1)
            self.images.append(l)

    def update(self):
        if not settings.updateGui:
            settings.updateGui = True
            self.frame.after(settings.guiUpdateInterval, self.update)
            return
        background = Image.open("snap_{},{}.tif".format(self.currentSet, 1))
        laser = Image.open("snap_{},{}.tif".format(self.currentSet, 2))
        shadow = Image.open("snap_{},{}.tif".format(self.currentSet, 3))
        result = Image.open("test3.png")  # SHOULD BE A RETURN FROM FUNCTION IN camera_math.py TODO TODO

        width = int(self.frame.winfo_width() / 2)
        height = int(self.frame.winfo_height() / 2)
        print(width,height)

        resultImg = ImageTk.PhotoImage(resize(result, width, height, Image.ANTIALIAS))
        backgroundImg = ImageTk.PhotoImage(resize(background.convert("RGB"), width, int(height/3), Image.LANCZOS))
        laserImg = ImageTk.PhotoImage(resize(laser.convert("RGB"), width, int(height/3), Image.LANCZOS))
        shadowImg = ImageTk.PhotoImage(resize(shadow.convert("RGB"), width, int(height/3), Image.LANCZOS))

        self.images[0].configure(image=resultImg)
        self.images[1].configure(image=backgroundImg)
        self.images[2].configure(image=laserImg)
        self.images[3].configure(image=shadowImg)

        self.images[0].image = resultImg
        self.images[1].image = backgroundImg
        self.images[2].image = laserImg
        self.images[3].image = shadowImg

        #self.currentSet += 1

        root.after(settings.guiUpdateInterval, self.update)

def resize(image_pil, width, height, mode):
    '''
    Resize PIL image keeping ratio and using white background.
    '''
    ratio_w = width / image_pil.width
    ratio_h = height / image_pil.height
    if ratio_w < ratio_h:
        # It must be fixed by width
        resize_width = width
        resize_height = round(ratio_w * image_pil.height)
    else:
        # Fixed by height
        resize_width = round(ratio_h * image_pil.width)
        resize_height = height
    image_resize = image_pil.resize(
        (resize_width, resize_height), mode)
    background = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    offset = (round((width - resize_width) / 2), round((height - resize_height) / 2))
    background.paste(image_resize, offset)
    return image_resize #background.convert('RGB')

q = QuantumGui()
