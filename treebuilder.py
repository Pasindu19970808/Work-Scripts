import pandas as pd

df = pd.read_excel(r'C:\Users\ASUS\Desktop\Python code\treetest.xlsx')



class Node:
    def __init__(self, nid, parent):
        self.nid = nid
        self.parent = parent
        self.children = []   
        

class buildtree:
    def addNodes(self,nodes):
        self.tree = {}
        for i in (1,2):
            for node in nodes:
                self.tree[node.nid] = node
                if node.parent in self.tree.keys():
                    if (node.parent != 'none') and (node not in self.tree[node.parent].children):
                        self.tree[node.parent].children.append(node)
        return self.tree
       
        
        
        
nodes = []
for nid,parent in tuple(zip(df.id,df.parent)):
    node = Node(nid,parent)
    nodes.append(node)

treebuilder = buildtree()
tree = treebuilder.addNodes(nodes)