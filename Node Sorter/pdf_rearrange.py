import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import fitz
from PIL import ImageTk
from PIL import Image
from tkinter import Canvas

class parentClass(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self)
        self.geometry('500x500')
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill = 'both', expand = True)

        self.display_frame = displayframe(self.main_frame,self)
        self.display_frame.grid(row = 1, column = 0, sticky = 'nsew')


class displayframe(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        
        self.button_frame = tk.LabelFrame(self)
        self.button_frame.pack(side = 'left', fill = 'both', padx = 10, pady = 10)
        
        self.right_frame = tk.LabelFrame(self)
        self.right_frame.pack(side = 'left',fill = 'both',padx = 10,pady = 10)

        self.top_right_frame = tk.LabelFrame(self.right_frame)
        self.top_right_frame.pack(side = 'top',fill = 'both', padx = 10, pady = 10)

        self.bottom_right_frame = tk.LabelFrame(self.right_frame)
        self.bottom_right_frame.pack(side = 'top', fill = 'both', padx = 10, pady = 10)

        self.left_scroll_frame = tk.LabelFrame(self.top_right_frame)
        self.left_scroll_frame.pack(side = 'left', fill = 'both', padx = 10,pady = 10)

        self.display_frame = tk.LabelFrame(self.top_right_frame)
        self.display_frame.pack(side = 'left', fill = 'both', padx = 10,pady = 10)

        self.right_scroll_frame = tk.LabelFrame(self.top_right_frame)
        self.right_scroll_frame.pack(side = 'left', fill = 'both', padx = 10,pady = 10)

        self.load_button = tk.Button(self.button_frame, text = 'Load PDF', command = lambda:self.loadPDF())
        self.load_button.grid(row = 1, column = 1, padx = 10, pady = 10)

        self.left_scroll_button = tk.Button(self.left_scroll_frame, text = "<")
        self.left_scroll_button.grid(row = 1, column = 1, padx = 10, pady = 10)

        #self.pdf_display = tk.Label(self.display_frame)
        #self.pdf_display.grid(row = 1, column = 1)

        self.right_scroll_button = tk.Button(self.right_scroll_frame, text = ">")
        self.right_scroll_button.grid(row = 1, column = 1, padx = 10, pady = 10)



    def loadPDF(self):
        self.pdf_path = filedialog.askopenfilename()
        if self.pdf_path != "":
            self.pdf = fitz.open(self.pdf_path)
            self.pix_list = [self.pdf[pg].get_pixmap() for pg in range(0,self.pdf.pageCount)]
            self.showpdf()
            #print('hi')

    def showpdf(self,pgnum = None):
        if pgnum is None:
            mode = "RGBA" if self.pix_list[0].alpha else "RGB"
            page_img = Image.frombytes(mode, [self.pix_list[0].width, self.pix_list[0].height],self.pix_list[0].samples)
            page_photo= ImageTk.PhotoImage(page_img)
            #self.pdf_display.configure(image = page_img)
            """ pix1 = fitz.Pixmap(self.pix_list[0], 0) if self.pix_list[0].alpha else self.pix_list[0]  # PPM does not support transparency
            imgdata = pix1.getImageData("ppm")  
            tkimg = tk.PhotoImage(data = imgdata) """
            canvas = Canvas(self.display_frame, width=page_img.size[0]+20, 
            height=page_img.size[1]+20)
            canvas.create_image(10, 10, anchor='nw', image=page_photo)
            canvas.pack(fill='both', expand=1)
            #self.pdf_display.configure(image = tkimg)

root = parentClass()
root.mainloop()