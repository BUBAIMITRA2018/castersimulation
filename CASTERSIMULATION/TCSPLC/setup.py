import sys
from cx_Freeze import setup, Executable

setup(
    name = "SMSSIMULATION",
    version = "3.7",
    description = "SIMULATION TOOLS USING OPCUA",
    executables = [Executable("TCS.py", base = "Win32GUI")])