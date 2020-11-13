import PyPDF2
import os
import tkinter as tk 
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

filepath  = filedialog.askdirectory()

os.chdir(filepath)

listoffiles = os.listdir(filepath)

listofneededfiles = [i for i in listoffiles if i.startswith('C') == True]
pdffile = PyPDF2.PdfFileWriter()

for file in listofneededfiles[:-1]:
    #pdf_file = open(file)
    read_pdf = PyPDF2.PdfFileReader(file,'rb')
    num_pages = read_pdf.getNumPages()
    pdffile.addPage(read_pdf.getPage(0))
    
with open('Compiled.pdf','wb') as abc:
    pdffile.write(abc)