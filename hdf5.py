''''

writing a HDF5 file 

'''


import numpy as np
import h5py
import os

os.chdir(r'C:\Users\pasindu.s\Desktop\FLACS')

d1 = np.random.random(size = (1000,33))
d2 = np.random.random(size = (1000,333))
d3 = np.random.random(size = (1000,3333))
hf = h5py.File('data.h5','w')

#hf.create_dataset('dataset_1',data = d1)
#hf.create_dataset('dataset_2',data = d2)

g1 = hf.create_group('group1/subfolder1')
g1.create_dataset('data1',data = d1)
g1.create_dataset('data2',data = d2)

g2 = hf.create_group('group2/subfolder2')
g2.create_dataset('data3',data = d3)


#hf.close()