import pandas as pd
import time
df = pd.read_excel(r'C:\Users\pasindu.s\Desktop\Mani Projects\NOSQLQuery.xlsx')

df.fillna(method = 'ffill',inplace = True)

class s1node:
    def __init__(self,hazard_type, hazard_category):
        self.haztype = hazard_type
        self.hazcategory = hazard_category
        
class buildtree:
    def addnodes(self,nodes):
        self.haztypeslist = list()
        #self.hazcatlist = list()
        self.tree = {}
        for node in nodes:
            if node.haztype not in self.haztypeslist:
                self.haztypeslist.append(node.haztype)
                self.tree[node.haztype] = list()
                '''
                The first instace a new hazard type is reached, a new hazard category list is created
                '''
                self.hazcatlist = list()
            '''
            The moment a new self.hazcatlist is created, this if statement becomes True and then we step in to add into the root hazard type.
            This prevents repetetively adding into the hazard type root
            '''
            if node.hazcategory not in self.hazcatlist:
                self.hazcatlist.append(node.hazcategory)
                self.tree[node.haztype].append(node.hazcategory)
        return self.haztypeslist, self.tree
        
        
        
        
        
#to find the root from the dictionary use list(s1tree.keys())




start = time.time()
s1rownodes = []
for (haztype,hazcat) in tuple(zip(df['Hazard Type'],df['Hazard Category'])):
    s1rownode = s1node(haztype,hazcat)
    s1rownodes.append(s1rownode)
    
    

s1treebuilder = buildtree()
haztypelist,s1tree = s1treebuilder.addnodes(s1rownodes)



with open('s1queries.txt','w') as s1queryfile:
    i = 1
    for haztype in s1tree:
        orderval = 1
        systemid = 1
        for orderval in range(len(s1tree[haztype])):
            hazcat = s1tree[haztype][orderval]
            masthaztypeid = list(s1tree.keys()).index(haztype) + 1
            query = 'db.MasterHazardCategoryType.insert('+'{' +\
            '"Index":{0}, "Order":{1}, "HazardCategoryType":"'.format(i,orderval + 1) +\
            '{0}", "SystemId":{1}, "MasterHazardTypeId":{2}, "ParendId":null'.format(hazcat,1,masthaztypeid)+'}'+');\n'
            s1queryfile.write(query)
            i +=1
s1queryfile.close()
        
end  = time.time()
print(end - start)

    
    
    
    
    
    
    
    
    

    
    
    
    
    
    
    
    
    
    