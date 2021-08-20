import cx_Freeze
import sys

base = None

if sys.platform == 'win32':
    base = "Win32GUI"
    
#defining the executables
executables = [cx_Freeze.Executable('Calculator.py',base=base, icon = 'Calculator.ico')]

cx_Freeze.setup(
        name = "Calculator",
        options = {"build_exe":{"packages":["tkinter"],"include_files":['Calculator.ico']}},
        version = "0.01",
        executables = executables             
        )