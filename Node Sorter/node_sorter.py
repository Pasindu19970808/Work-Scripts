import fitz
import pandas as pd
import os
from tkinter import filedialog


current = filedialog.askdirectory(title = 'Select Folder to save files')
#r"C:\\Users\\pasindu.s\\Desktop\\Work-Scripts\\Node Sorter\\AGRU_Nodes.csv"
binder_file_name = filedialog.askopenfilename(title = 'Select Binder PDF(Only One file)')

csv_file_name = filedialog.askopenfilename(title = 'Select CSV file with node list')

#binderpdf = PyPDF2.PdfFileReader("Acid Gas Removal Unit_Node mark-up_31Mar2021.pdf",'rb')


if (current != "") & (binder_file_name != "") & (csv_file_name != ""):
    doc = fitz.open(binder_file_name)
    node_df = pd.read_csv(csv_file_name)
    node_list = node_df["Nodes"].tolist()
    for node in node_list:
        node_pg_count = list()
        nodefile = fitz.open()
        for i in range(0,doc.pageCount):
            pg = doc[i]
            for annot in pg.annots():
                if((annot.type[1] == 'FreeText') & (node in annot.info["content"].split(" "))):
                    node_pg_count.append(i)
        if (len(node_pg_count) != 0):
            for pg_num in node_pg_count:
                nodefile.insert_pdf(doc,pg_num,pg_num,annots=True)
                #nodefile.save()
            #nodefile.insert_pdf(doc, extract_pg])
            path = os.path.join(current,node)
            os.makedirs(path)
            pdf_path = os.path.join(path,node + '.pdf')
            nodefile.save(pdf_path)
            nodefile.close()
        #with open(pdf_path,'wb') as abc:
        #    nodefile.write(abc)