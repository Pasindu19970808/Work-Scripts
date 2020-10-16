import pandas as pd
import time 



class produnique:
    def produce_uniq(seq):
        seen = set()
        return [x for x in seq if x not in seen and not seen.add(x)]

class create_node:
    def __init__(self,hazardtype):
        self.parentname = hazardtype
        self.children = []
     
class create_rownode:
    def __init__(self,hazard_type, hazard_category, guideword):
        self.rowparent = hazard_type
        self.rowchild = hazard_category
        self.rowgrandchild = guideword
        
        
class create_tree(create_node):
    def __init__(self,parentnodes,rownodes):
        temp = None
        for parentnode in parentnodes:
            i = -1
            for rownode in rownodes:
                if rownode.rowparent == parentnode.parentname and rownode.rowchild != temp:
                    #childnode = create_node(rownode.rowchild)
                    temp = rownode.rowchild
                    parentnode.children.append(create_node(temp))
                    i +=1
                try:
                    if rownode.rowchild == parentnode.children[i].parentname:
                        parentnode.children[i].children.append(rownode.rowgrandchild)
                except:
                    continue
        #self.result = parentnode
        #return self.result  
start = time.time()          
df = pd.read_excel(r'C:\Users\pasindu.s\Desktop\Mani Projects\NOSQLQuery.xlsx')

haztypes = list(df['Hazard Type'])


df.fillna(method = 'ffill',inplace = True)
       

haztypes_unique = produnique.produce_uniq(haztypes)
haztypes_unique.pop(1)

parentnodes = []
for haztype in haztypes_unique:
    parentnode = create_node(haztype)
    parentnodes.append(parentnode)

rownodes = []
for (hazard_type, hazard_category, guideword) in tuple(zip(df['Hazard Type'],df['Hazard Category'],df['Guidewords'])):
     rownode = create_rownode(hazard_type, hazard_category, guideword)
     rownodes.append(rownode)

create_tree(parentnodes, rownodes)
end = time.time()

print(end - start)