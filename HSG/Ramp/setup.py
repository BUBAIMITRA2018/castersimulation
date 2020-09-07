import sys
from cx_Freeze import setup, Executable

setup(
    name = "SMSSIMULATION",
    version = "3.7",
    description = "SIMULATION TOOLS USING OPCUA",
    executables = [Executable("Ramp.py", base = "Win32GUI")])