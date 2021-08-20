import pandas as pd
import numpy as np
import os
from tkinter import filedialog
import tkinter as tk
from tkinter import messagebox
import sys

class parentClass(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.geometry('250x400')
        self.title("FRA Cumulative Frequency")
        self.fracontainer = tk.Frame(self)
        self.fracontainer.pack(fill = 'both', expand = True)

        mainframe= mainFrame(self.fracontainer,self)
        mainframe.grid(row = 1, column = 0, sticky = 'nsew')
class mainFrame(tk.Frame):
    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent)
        self.jf_frame = tk.LabelFrame(self)
        self.jf_frame.pack(side = 'top', fill = 'both',padx = 10,pady = 10)
        self.pf_frame = tk.LabelFrame(self)
        self.pf_frame.pack(side = 'top', fill = 'both',padx = 10,pady = 10)
        self.jfbutton = tk.Button(self.jf_frame, text = "Select JF Master File", command= lambda:self.get_jf_path())
        self.jfbutton.grid(row = 1, column = 1, padx = 60, pady = 10)
        self.pfbutton = tk.Button(self.pf_frame, text = "Select PF Master File", command= lambda:self.get_pf_path())
        self.pfbutton.grid(row = 1, column = 1, padx = 60, pady = 10)
        self.finalframe = tk.LabelFrame(self)
        self.finalframe.pack(side = 'top', fill = 'both',padx = 10,pady = 10)
        self.finalbutton = tk.Button(self.finalframe, text = "Process", command= lambda:self.produce_dataframe())
        self.finalbutton.grid(row = 1, column = 1, padx = 60, pady = 10)
        self.statusframe = tk.LabelFrame(self)
        self.statusframe.pack(side = 'top', fill = 'both',padx = 10,pady = 10)
        self.status = tk.Label(self.statusframe, text= "Upload Files", justify = "center")
        self.status.grid(row = 1, column = 1, padx = 60, pady = 10)

        self.excelframe = tk.LabelFrame(self)
        self.excelframe.pack(side = 'top', fill = 'both',padx = 10,pady = 10)
        self.excelbutton = tk.Button(self.excelframe, text = "Produce Excel Workbook",state='disabled', command= lambda: self.produce_excel())
        self.excelbutton.grid(row = 1, column = 1, padx = 60, pady = 10)
       
    def get_jf_path(self):
        self.jf_file = filedialog.askopenfilename(title = "Select the Jetfire Master")
    
    def get_pf_path(self):
        self.pf_file = filedialog.askopenfilename(title = "Select the PoolFire Master")

    def produce_dataframe(self):
        try:
            self.status.config(text = "Started Processing")
            #get data
            df_master_exceedance_jf = pd.read_excel(self.jf_file, engine = "openpyxl",sheet_name="Exceedance Log")
            df_master_receiver_jf = pd.read_excel(self.jf_file, engine = "openpyxl",sheet_name="Receiver Points")
            df_master_exceedance_pf = pd.read_excel(self.pf_file, engine = "openpyxl", sheet_name = "Exceedance Log")
            df_master_receiver_pf = pd.read_excel(self.pf_file, engine = "openpyxl", sheet_name = "Receiver Points")

            header_2 = df_master_exceedance_jf.iloc[0,:].tolist()
            columns = ['Receiver ID','Hazard ID','Consequence Type','Hazard Location','Frequency','Distance','Consequence Time','Hazard','Hazard','Hazard','Receiver','Receiver','Receiver']
            columns_combined = list()
            for head,head2 in zip(header_2,columns):
                if pd.isna(head):
                    columns_combined.append(head2)
                else:
                    columns_combined.append("_".join([head2,head]))
            
            df_master_exceedance_jf.columns = columns_combined
            df_master_exceedance_jf.drop(index=[0],axis = 0,inplace = True)
            df_master_exceedance_pf.columns = columns_combined
            df_master_exceedance_pf.drop(index=[0],axis = 0,inplace = True)

            df_master_receiver_jf.columns = df_master_receiver_jf.iloc[0,:].tolist()
            df_master_receiver_jf.drop(index = [0], axis = 0, inplace = True)
            df_master_receiver_pf.columns = df_master_receiver_pf.iloc[0,:].tolist()
            df_master_receiver_pf.drop(index = [0], axis = 0, inplace = True)

            unique_receivers_pf = df_master_receiver_pf["Receiver ID"].unique().tolist()
            unique_receivers_jf = df_master_receiver_jf["Receiver ID"].unique().tolist()

            required_columns = ['Receiver ID','Hazard ID','Consequence Type','Hazard Location','Frequency','Distance','Consequence Time']
            self.jf_exceedance = None
            self.pf_exceedance = None
            for receiver in unique_receivers_jf:
                temp_jf = df_master_exceedance_jf.loc[df_master_exceedance_jf["Receiver ID"] == receiver].sort_values(by=["Receiver ID","Consequence Time"])[required_columns]
                if self.jf_exceedance is None:
                    self.jf_exceedance = temp_jf
                else:
                    self.jf_exceedance = self.jf_exceedance.append(temp_jf, ignore_index = False)

            for receiver in unique_receivers_pf:
                temp_pf = df_master_exceedance_pf.loc[df_master_exceedance_pf["Receiver ID"] == receiver].sort_values(by=["Receiver ID","Consequence Time"])[required_columns]
                if self.pf_exceedance is None:
                    self.pf_exceedance = temp_pf
                else:
                    self.pf_exceedance = self.pf_exceedance.append(temp_pf, ignore_index = False)

            self.jf_exceedance.reset_index(drop = True, inplace = True)
            self.pf_exceedance.reset_index(drop = True, inplace = True)

            columns_template = ['Receiver ID JF','Hazard ID JF','Frequency JF','Consequence Time JF','Heat Dose JF','Cumulative Frequency JF','Receiver ID PF','Hazard ID PF','Frequency PF','Consequence Time PF','Heat Dose PF','Cumulative Frequency PF']
            row_num = self.jf_exceedance.shape[0] if self.jf_exceedance.shape[0] > self.pf_exceedance.shape[0] else self.pf_exceedance.shape[0]
            data = np.empty(shape = (row_num,len(columns_template)))
            data[:] = np.nan
            self.template_df = pd.DataFrame(data = data, columns = columns_template)

            self.template_df.iloc[0:self.jf_exceedance.shape[0],0:4] = self.jf_exceedance[['Receiver ID','Hazard ID','Frequency','Consequence Time']]
            self.template_df.iloc[0:self.pf_exceedance.shape[0],6:10] = self.pf_exceedance[['Receiver ID','Hazard ID','Frequency','Consequence Time']]
            self.template_df["Heat Dose JF"] = 250 * self.template_df["Consequence Time JF"] * 60
            self.template_df["Heat Dose PF"] = 100 * self.template_df["Consequence Time PF"] * 60

            self.template_df.iloc[0:self.jf_exceedance.shape[0]]["Cumulative Frequency JF"] = np.flip(np.cumsum(np.flip(self.template_df.iloc[0:self.jf_exceedance.shape[0]]["Frequency JF"])))
            self.template_df.iloc[0:self.pf_exceedance.shape[0]]["Cumulative Frequency PF"] = np.flip(np.cumsum(np.flip(self.template_df.iloc[0:self.pf_exceedance.shape[0]]["Frequency PF"])))

            total_rows = self.jf_exceedance.shape[0] + self.pf_exceedance.shape[0]
            columns_final = ["Receiver ID","Frequency","Consequence Time", "Heat Dose"]
            data_final = np.empty(shape = (total_rows, len(columns_final)))
            data_final[:] = np.nan
            self.final_df = pd.DataFrame(data = data_final, columns = columns_final)

            self.final_df.iloc[0:self.jf_exceedance.shape[0],:] = self.template_df.iloc[0:self.jf_exceedance.shape[0]][["Receiver ID JF","Frequency JF","Consequence Time JF","Heat Dose JF"]]
            self.final_df.iloc[self.jf_exceedance.shape[0]:self.final_df.shape[0],:] = self.template_df.iloc[0:self.pf_exceedance.shape[0]][["Receiver ID PF","Frequency PF","Consequence Time PF","Heat Dose PF"]]

            self.final_df = self.final_df.sort_values(by = "Heat Dose", ignore_index = True)
            self.final_df["Cumulative Frequency"] = np.nan
            self.final_df["Cumulative Frequency"] = np.flip(np.cumsum(np.flip(self.final_df["Frequency"])))

            self.status.config(text = "Completed Processing")
            self.excelbutton.config(state = "normal")
        except:
            messagebox.showerror('Error',",".join(sys.exc_info()))


    def produce_excel(self):
        self.savingdirectory = filedialog.askdirectory(title="Select Directory to Save File")
        if(self.savingdirectory != ""):
            #with pd.ExcelWriter(os.path.join(self.savingdirectory,'FRA_Processed.xlsx')) as writer:
            self.jf_exceedance.to_csv(os.path.join(self.savingdirectory,"JF_Exceedance.csv"), index = False)
            self.pf_exceedance.to_csv(os.path.join(self.savingdirectory,"PF_Exceedance.csv"), index = False)
            self.template_df.to_csv(os.path.join(self.savingdirectory,"JFPF_CumulFreq.csv"), index = False)
            self.final_df.to_csv(os.path.join(self.savingdirectory,"CumulFreq.csv"), index = False)
            self.status.config(text = "Excel Produced")
        else:
            messagebox.showerror('Error',"Select Save Directory")
        



root = parentClass()
root.mainloop()





""" if ((jf_file != "") & (pf_file != "")):
    df_master_exceedance_jf = pd.read_excel(jf_file, engine = "openpyxl",sheet_name="Exceedance Log")
    df_master_receiver_jf = pd.read_excel(jf_file, engine = "openpyxl",sheet_name="Receiver Points")
    df_master_exceedance_pf = pd.read_excel(pf_file, engine = "openpyxl", sheet_name = "Exceedance Log")
    df_master_receiver_pf = pd.read_excel(pf_file, engine = "openpyxl", sheet_name = "Receiver Points")

      """