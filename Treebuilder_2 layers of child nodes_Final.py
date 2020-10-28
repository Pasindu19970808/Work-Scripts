import pandas as pd
import time 

#instead of col name have index
#

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


with open('s1queries_v1.txt','w') as s1queryfile, open('s2queries_v1.txt','w') as s2queryfile:
    indexnum = 1
    indexnums2 = 1
    for i in range(len(parentnodes)):
        for childnode in parentnodes[i].children:
            orderval = parentnodes[i].children.index(childnode) + 1
            hazcat = childnode.parentname
            masthaztypeid = i + 1
            query1 = 'db.MasterHazardCategoryType.insert('+'{' +\
            '"Index":{0}, "Order":{1}, "HazardCategoryType":"'.format(indexnum,orderval) +\
            '{0}", "SystemId":"1", "MasterHazardTypeId":"'.format(hazcat) +\
            '{0}", "ParendId":null'.format(masthaztypeid)+'}'+');\n'
            s1queryfile.write(query1)
            for grandchild in childnode.children:
                ordervals2 = childnode.children.index(grandchild) + 1
                guideword = grandchild
                #MasterHazardTypeID = masthaztypeid
                #CategoryTypeID = orderval
                syshaztypeid = str(masthaztypeid) + str(orderval)
                query2 = 'db.MasterHazardCategoryType.insert('+'{' +\
                '"Index":{0}, "Order":{1}, "GuideWordName":"'.format(indexnums2,ordervals2) +\
                '{0}", "SystemId":"1", "MasterHazardTypeId":"'.format(guideword) +\
                '{0}", "CategoryTypeID":"'.format(masthaztypeid)+\
                '{0}", "SystemHazardTypeID":"'.format(indexnum)+\
                '{0}"'.format(str(masthaztypeid) + str(indexnum))+'}'+');\n'
                s2queryfile.write(query2)
                indexnums2 +=1
            indexnum += 1
                
s1queryfile.close()
s2queryfile.close()
        
end = time.time()

print(end - start)
       
        
        
        
        
        
        
        
'''
        
query = 'db.MasterHazardCategoryType.insert('+'{' +\
            '"Index":{0}, "Order":{1}, "HazardCategoryType":"'.format(indexnum,orderval + 1) +\
            '{0}", "SystemId":{1}, "MasterHazardTypeId":{2}, "ParendId":null'.format(hazcat,1,masthaztypeid)+'}'+');\n'
    
'''




























