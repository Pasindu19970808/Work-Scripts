#https://docs.python.org/3/tutorial/modules.html
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
import DataHash
from getmac import get_mac_address as gma
import os
import re
class parentClass(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        #create a container to pack your first frame into 
        self.geometry('250x300')
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
        #self.macaddress = ''.join([j.upper() for j in ['-' if i == ':' else i for i  in list(gma())]])
        self.macstring = tk.StringVar()
        self.macstring.set("Enter MAC Address")
        self.macaddress = tk.Entry(self.macaddressframe, textvariable=self.macstring, width = 30) 
        self.macaddress.pack(side = 'left', fill = 'both',padx = 10, pady = 10)
        #self.testlabel = tk.Label(self.macaddressframe, text = self.macaddress, padx = 10, pady = 10)
        #self.testlabel.grid(row = 1, column = 1)

        self.yearframe  = tk.LabelFrame(self)
        self.yearframe.pack(side = 'top',fill = 'both', padx = 10, pady = 10)
        self.selectyearlabel = tk.Label(self.yearframe, text = 'Select Year', padx = 10, pady = 10)
        self.selectyearlabel.grid(row = 2, column = 0)
        self.yearvar = tk.StringVar()
        self.yearmenu = tk.OptionMenu(self.yearframe,self.yearvar,())
        self.yearmenu.grid(row = 2, column = 1)
        yearmenu = self.yearmenu['menu']
        yearlist = [str(i) for i in list(range(2000,2100))]
        [yearmenu.add_command(label = year, command = lambda value = year:self.yearvar.set(value)) for year in yearlist]
        self.yearvar.set('Select Year')

        self.monthframe  = tk.LabelFrame(self)
        self.monthframe.pack(side = 'top',fill = 'both', padx = 10, pady = 10)
        self.selectmonthlabel = tk.Label(self.monthframe, text = 'Select Month', padx = 10, pady = 10)
        self.selectmonthlabel.grid(row = 3, column = 0)
        self.monthvar = tk.StringVar()
        self.monthmenu = tk.OptionMenu(self.monthframe,self.monthvar,())
        self.monthmenu.grid(row = 3, column = 1)
        monthmenu = self.monthmenu['menu']
        monthlist = [str(i) for i in list(range(1,13))]
        [monthmenu.add_command(label = month, command = lambda value = month:self.monthvar.set(value)) for month in monthlist]
        self.monthvar.set('Select Month')

        self.buttonframe = tk.LabelFrame(self)
        self.buttonframe.pack(side = 'top', fill = 'both', padx = 10, pady = 10)
        self.generateButton = tk.Button(self.buttonframe, text = 'Generate Hash', command = lambda: self.generateHash())
        self.generateButton.grid(row = 1, column = 1, padx = 60, pady = 10)


    def generateHash(self):
        sanitycheck = False
        if(len(re.findall(r'[^0-9A-Z-]',self.macstring.get().strip())) == 0):
            sanitycheck = True
        if ((self.yearvar.get() != 'Select Year') & (self.monthvar.get() != 'Select Month') & sanitycheck == True):
            savepath = filedialog.askdirectory()
            os.chdir(savepath)
            datahasher = DataHash.datahash()
            dataarray = list()
            dataarray.append(str(self.macstring.get().strip()))
            dataarray.append(self.yearvar.get())
            dataarray.append(self.monthvar.get())
            with open('license.lic','w') as licfile:
                licfile.write(datahasher.hashing(dataarray))
            licfile.close()
        elif(sanitycheck == False):
            messagebox.showerror('Error','Invalid MAC Address entered')
        else:
            messagebox.showerror('Error','Select Year and Month')


root = parentClass()
root.mainloop()
#test = DataHash.datahash()
