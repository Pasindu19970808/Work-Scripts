import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"
    
#defining the executables
executables = [cx_Freeze.Executable('FRA_frequencycalc.py',base=base)]

cx_Freeze.setup(
        name = "Calculator",
        options = {"build_exe":{"packages":["tkinter"]}},
        version = "0.01",
        executables = executables             
        )