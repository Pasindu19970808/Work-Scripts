#pumpernickel90-B1-1C-99-F1-6620214
import hashlib
import numpy as np
class datahash:
    def __init__(self):
        #[Salt, mac address, year in string format, month number in string format]
        
        self.Method = "MD5"
        self.OutFormat = 'hex'
        self.isFile = False
        self.isBin = False

    def hashing(self,dataarray):
        #dataarray is a list
        #md5 object 
        self.data = dataarray
        if (type(dataarray) == list):
                hashlib_object = hashlib.md5()
                dataarraystring = ''.join(dataarray)
                self.CoreHash(dataarraystring,hashlib_object)
        else:
            raise TypeError("Dataarray needs to be of type list")

    def CoreHash(self, dataarraystring, hashlib_object):
        #data coming in will always be of string type
        #as this is being reproduced using MATLAB, only with specific lines of code in mind, the first part will be hardcoded
        #string in Matlab is taken as char
        #MATLAB code
        #Engine.update([uint8(class(Data)), typecast(size(Data), 'uint8')])

        asciibytearray = [ord(i) for i in list('char')]
        shape_dim1 = 1
        shape_dim2 = np.array(list(dataarraystring)).shape[0]
        #The mapping of double datatype in MATLAB is equivalent to Float in Python
        #Each byte consists of 64 bits in MATLAB
        #Make a numpy array of np.float64 mapping
        #convert to np. to make it unsigned integer of 8 bit per byte format
        datasize_int8 = np.array([shape_dim1,shape_dim2],dtype = np.float64).view(np.uint8)
        np.append(np.array(asciibytearray).view(np.uint8)[[0,4,8,12]],datasize_int8.reshape(1,-1))

        pass