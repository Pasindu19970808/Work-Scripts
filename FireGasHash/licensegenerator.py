#https://docs.python.org/3/tutorial/modules.html
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import DataHash
from getmac import get_mac_address as gma

class parentClass(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        #create a container to pack your first frame into 
        self.geometry('200x200')
        self.title('License Generator')
        self.licContainer = tk.Frame(self)
        self.licContainer.pack(fill = 'both', expand = True)

        licgeneratorframe = licenseframe(self.licContainer,self)
        licgeneratorframe.grid(row = 1, column = 0, sticky = 'nsew')


class licenseframe(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)

        self.macaddressframe = tk.LabelFrame(self)
        self.macaddressframe.pack(side = 'top', fill = 'both', padx = 10, pady = 10)
        self.macaddress = ''.join([j.upper() for j in ['-' if i == ':' else i for i  in list(gma())]])
        self.testlabel = tk.Label(self.macaddressframe, text = self.macaddress, padx = 10, pady = 10)
        self.testlabel.grid(row = 1, column = 1)

        self.monthframe  = tk.LabelFrame(self)
        self.monthframe.pack(side = 'top',fill = 'both', padx = 10, pady = 10)
        self.selectyearlabel = tk.Label(self.monthframe, text = 'Select Year', padx = 10, pady = 10)
        self.selectyearlabel.grid(row = 2, column = 0)
        self.yearvar = tk.StringVar()
        self.yearmenu = tk.OptionMenu(self.monthframe,self.yearvar,())
        self.yearmenu.grid(row = 2, column = 1)
        yearmenu = self.yearmenu['menu']
        yearlist = [str(i) for i in list(range(2000,2100))]
        [yearmenu.add_command(label = year, command = lambda value = year:self.yearvar.set(value)) for year in yearlist]
        self.yearvar.set('Select Year')
        #self.testlabel2 = tk.Label(self.monthframe, text = 'Upload Weather Data Txt Files', padx = 10, pady = 10)
        #self.testlabel2.grid(row = 1, column = 1)


root = parentClass()
root.mainloop()
#test = DataHash.datahash()
