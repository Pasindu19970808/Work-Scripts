import tkinter as tk
import PyPDF2 as pdf
import tkinter.filedialog as tkfile


class Mainwindowclass(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        container  = tk.Frame(self)
        container.pack(side = 'top', fill = 'both', expand = True)
        self.geometry("900x800")
        
        self.frames = {}
        
        firstpageframe = firstpage(container,self)
        
        self.frames[firstpage] = firstpageframe
        firstpageframe.grid(row = 0, column = 0, sticky = 'nsew')
        self.show_frame(firstpage)
        
    def show_frame(self, framename):
        frame = self.frames[framename]
        frame.tkraise()

class firstpage(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.loadedproposalpdflist = list()
        self.loadedbrochurelist = list()
        self.loadedCVlist = list()
        
        self.cvpagenum = list()
        self.proposalinputframe = tk.LabelFrame(self,padx = 10, pady = 10)
        self.proposalinputframe.pack(side = 'top', fill = 'x')
        
        self.brochureinputframe = tk.LabelFrame(self,padx = 10, pady = 10)
        self.brochureinputframe.pack(side = 'top', fill = 'x')
        
        self.cvinputframe = tk.LabelFrame(self, padx = 10, pady = 10)
        self.cvinputframe.pack(side = 'top',fill = 'x')
        
        self.loadedframe = tk.LabelFrame(self, padx = 10, pady = 10)
        self.loadedframe.pack(side = 'top', fill = 'x')
        
        #for loading proposals
        self.loadproposallabel = tk.Label(self.proposalinputframe, text = 'Proposal File Path', padx = 10, pady = 10, bg = 'red4',bd = 10)
        self.loadproposallabel.pack(side = 'left')
        
        self.proposalfilepathname = tk.StringVar()
        self.proposalentrydisplay = tk.Entry(self.proposalinputframe, relief = 'sunken', width = 80,textvariable = self.proposalfilepathname)
        self.proposalentrydisplay.pack(side = 'left')
                
        self.proposalloadbutton = tk.Button(self.proposalinputframe, text = 'Load Proposal Template PDF File', padx = 10, pady = 10, command = lambda: self.loadproposalpdf())
        self.proposalloadbutton.pack(side = 'left')
        
        #for loading brochure
        self.loadbrochurelabel = tk.Label(self.brochureinputframe, text = 'Brochure File Path', padx = 10, pady = 10, bg = 'red4',bd = 10)
        self.loadbrochurelabel.pack(side = 'left')
        
        self.brochurefilepathname = tk.StringVar()
        self.brochureentrydisplay = tk.Entry(self.brochureinputframe, relief = 'sunken', width = 80,textvariable = self.brochurefilepathname)
        self.brochureentrydisplay.pack(side = 'left')
                
        self.brochureloadbutton = tk.Button(self.brochureinputframe, text = 'Load Brochure', padx = 10, pady = 10, command = lambda: self.loadbrochurepdf())
        self.brochureloadbutton.pack(side = 'left')
        
        #for loading cvs
        self.loadcvlabel = tk.Label(self.cvinputframe, text = 'CV File Path', padx = 10, pady = 10, bg = 'red4',bd = 10)
        self.loadcvlabel.pack(side = 'left')
        
        self.cvfilepathname = tk.StringVar()
        self.cventrydisplay = tk.Entry(self.cvinputframe, relief = 'sunken', width = 80,textvariable = self.cvfilepathname)
        self.cventrydisplay.pack(side = 'left')
                
        self.cvloadbutton = tk.Button(self.cvinputframe, text = 'Load Brochure', padx = 10, pady = 10, command = lambda: self.loadcvpdf())
        self.cvloadbutton.pack(side = 'left')
        
        
        
        #loadedsection
        self.loadedlabel = tk.Label(self.loadedframe,padx = 10, pady = 10, text = 'Loaded Proposal:')
        self.loadedlabel.grid(row = 1, column = 1)
        
        self.loadedproposalpdffilepaths = tk.StringVar()
        self.loadedproposalpdffilepaths.set('No PDFs selected for compiling')
        self.loadedproposalpdfdisplay = tk.Message(self.loadedframe, padx = 10, pady = 10, width = 500, text = self.loadedproposalpdffilepaths.get())
        self.loadedproposalpdfdisplay.grid(row = 2, column = 1)
        
        self.proposalpdfpagenumber = tk.StringVar()
        self.proposalpdfpagenumber.set('0')
        self.proposalpdfpagenumberdisplay = tk.Message(self.loadedframe, padx = 10, pady = 10, width = 50, text = self.proposalpdfpagenumber.get())
        self.proposalpdfpagenumberdisplay.grid(row = 2, column = 2)
        
        
    
    def loadproposalpdf(self):
        if len(self.loadedproposalpdflist) < 1:
            pdffilepath = tkfile.askopenfile(mode = 'r', filetypes = (('All Files','*'),))
            #self.pdfpagenum.append(str((pdf.PdfFileReader(open(pdffilepath.name,'rb'))).getNumPages()))
            self.loadedproposalpdflist.append(pdffilepath.name)
            self.proposalfilepathname.set(pdffilepath.name)
            self.loadedproposalpdffilepaths.set('\n'.join(self.loadedproposalpdflist))
            self.loadedproposalpdfdisplay.config(text = self.loadedproposalpdffilepaths.get())
            self.proposalpdfpagenumber.set(str(pdf.PdfFileReader(open(pdffilepath.name,'rb')).getNumPages()))
            self.proposalpdfpagenumberdisplay.config(text = self.proposalpdfpagenumber.get())
        else:
            tk.messagebox.askokcancel('Attention', 'You have already loaded a template proposal')
    
    def loadbrochurepdf():
        #if len(self.loadedbrochurelist) < 1:
         return   
            
    def loadcvpdf():
        #if len(self.loadedbrochurelist) < 1:
         return   
        


root = Mainwindowclass()
root.mainloop()