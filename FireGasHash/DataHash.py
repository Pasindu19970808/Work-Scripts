import hashlib
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






        pass