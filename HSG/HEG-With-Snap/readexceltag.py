import pandas as pd
from logger import *

import sys, os

import logging
import traceback as trace
import xlrd
import time
from opcua import Client
from time import sleep
from opcua import ua

setup_logging_to_file("main.log")

# df1S= pandas.read_excel('Working_VF1.xls', sheet_name='Tag List')
# my_logger = logging.getLogger("SOV1D LOGS HERE")
# my_logger.setLevel(logging.INFO)
#
#
#
# def log_app_error(e:BaseException,level = logging.ERROR):
#     e_traceback = trace.format_exception(e.__class__,e,e.__traceback__)
#     traceback_lines = []
#     for line in [line.rstrip('\n')for line in e_traceback]:
#         traceback_lines.extend(line.splitlines())
#     logging.log(level,e.args,traceback_lines.__str__())





class Valves:


    def __init__(self,tagslist):
        self._taglist = tagslist
        self.readdata=[]
        self.setup()
        self.process()




    def setup(self):
        try:
            self.df = pd.read_excel(r'D:\OPCUA\Working_VF1.xls', sheet_name='Valve1S')
            row,col = self.df.shape

            print(f"col number is : {col}")


        except Exception as e :
            log_exception(e)



    def process(self):

       for i in self.readcmd():
           print(i)







    def readcmd(self):
        n = 0
        while n<len(self.df.index):
            data = self.df.iloc[n,3]
            yield data
            n= n+1












    def searchValueBytag(self,cmdtag):
         for item in self._taglist:
             # print(f"item is {item[0]}")
             # print(f"cmd tag is :{cmdtag}")
             if item[0] == cmdtag:
                 pass


             else:
                pass











taglist = [('MABunk7DedFlpOpnCmd',False),('MABunk7DedFlpClsCmd',True)]

print(len(taglist))




valv = Valves(taglist)
































# df = pd.read_excel(r'D:\OPCUA\Working_VF1.xls', sheet_name='Valve1S')
#
# my_list = [(4,5),(6,7),(7,8)]
#
# def iter_list(list):
#     x = len(my_list)
#     for y in my_list :
#         for i in y:
#             if i == 6:
#                 print(i+1)
#                 break







# iter_list(my_list)

        # if i[0] == value:
        #     print(f"tag value is: {j[1]}")





# df1D=pandas.read_excel(r'D:\python\prgrms\Working_VF1 - Copy1.xls', sheet_name='Motor1D')
# df2D=pandas.read_excel(r'D:\python\prgrms\Working_VF1 - Copy1.xls', sheet_name='Motor2D')
# dfcv=pandas.read_excel(r'D:\python\prgrms\Working_VF1 - Copy1.xls', sheet_name='ControlValves')
# dfat=pandas.read_excel(r'D:\python\prgrms\Working_VF1 - Copy1.xls', sheet_name='AnalogTx')
# dc=pandas.read_excel(r'D:\python\prgrms\Working_VF1 - Copy1.xls', sheet_name='ReadGeneral')
# for i in dc.index:
#         url=dc['OPCServer'][i]
#         print(url)
#         print("Connected")
#         break
# client=Client(url)
# client.connect()
# def fn_Valve1S(CompName,Cmd,OpenFb,CloseFb,DelayTime):
#     if(Cmd==0):
#             CloseFb=1
#             OpenFb=0
#     if(Cmd==1):
#             sleep(DelayTime)
#             CloseFb=0
#             OpenFb=1
#
# '''
# def fn_Valve2S(CompName,OpnCmd,ClsCmd,OpenFb,CloseFb,DelayTime):
#     if(OpnCmd==1 and ClsCmd==0):
#
#         sleep(DelayTime)
#         OpenFb=1
#         CloseFb=0
#     elif(OpnCmd==0 and ClsCmd==1):
#         OpenFb=0
#         ClosFb=1
#     else:
#         print("Sorry wrong value")
# def fn_Motor1D(CompName,OnCmd,RunFb,HealthyFb,ReadyFb,MCCBOnFb,OverloadFb,FaultFb,DelayTime):
#     if(OnCmd==1):
#         sleep(DelayTime)
#
#         RunFb=1
#         HealthyFb=1
#         ReadyFb=1
#         MCCBOnFb=1
#         OverloadFb=0
#         FaultFb=0
#     elif(OnCmd==0):
#         RunFb=0
#         HealthyFb=1
#         ReadyFb=1
#         MCCBOnFb=1
#         OverloadFb=0
#         FaultFb=0
#
# def fn_Motor2D(CompName,FwdCmd,RevCmd,FwdRunFb,RevRunFb,HealthyFb,ReadyFb,MCCBOnFb,OverloadFb,FaultFb,DelayTime):
#     if(FwdCmd==1 and RevCmd==0):
#         sleep(DelayTime)
#
#         FwdRunFb=1
#         HealthyFb=1
#         ReadyFb=1
#         MCCBOnFb=1
#         OverloadFb=0
#         FaultFb=0
#
#     if(FwdCmd==0 and RevCmd==1):
#         RevRunFb=1
#         HealthyFb=1
#         ReadyFb=1
#         MCCBOnFb=1
#         OverloadFb=0
#         FaultFb=0
# def fn_ControlValves(SP,PV,DEelayTime):
#     ReturnValue=SP
#     if(PV<SP):
#         PV=ReturnValue
#     else:
#         PV=ReturnValue
# def fn_AnalogTx(HighLim,LowLim,Val,SelVal,OutAna):
#     if(SelVal==1):
#         OutAna=Val
#     if(SelVal==0):
#         if(SelVal>=HighLim):
#             selVal=LowLim
#             #SelVal=Val
#         else:
#             SelVal=SelVal+1
#             #SelVal=Val
#
# '''
#
# while True:
#     for index, row in df1S.iterrows():
#             b1S=(row['CompName'])
#             c1S=(row['Cmd'])
#             d1S=(row['OpenFb'])
#             e1S=(row['CloseFb'])
#             f1S=(row['DelayTime'])
#             #print(b1S)
#            #print(c1S)
#             #print(d1S)
#             #print(e1S)
#             #print(f1S)
#             r='BotStirLoop12VlvOpnCmd'
#             path=['7:BOF-P']
#
#             root = client.get_root_node()
#             print(root)
#             myvar = root.get_child(["0:Objects","1:SYM","7:BOF-P","7:c1S"])
#             print(myvar)
#             var = root.get_value()
#             print(var)
#             print(fn_Valve1S(b1S,c1S,d1S,e1S,f1S))
#             sleep(2)
#
#
#
#
# '''
#     for index, row in df2S.iterrows():
#             b2S=(row['CompName'])
#             c2S=(row['OpnCmd'])
#             d2S=(row['ClsCmd'])
#             e2S=(row['OpenFb'])
#             f2S=(row['CloseFb'])
#             g2S=(row['DelayTime'])
#             print(b2S)
#             print(c2S)
#             print(d2S)
#             print(e2S)
#             print(f2S)
#             print(g2S)
#             print(fn_Valve2S(b2S,c2S,d2S,e2S,f2S,g2S))
#             sleep(5)
#     for index, row in df1D.iterrows():
#             b1D=(row['CompName'])
#             c1D=(row['OnCmd'])
#             d1D=(row['RunFb'])
#             e1D=(row['HealthyFb'])
#             f1D=(row['ReadyFb'])
#             g1D=(row['MCCBOnFb'])
#             h1D=(row['OverloadFb'])
#             i1D=(row['FaultFb'])
#             j1D=(row['DelayTime'])
#             print(b1D)
#             print(c1D)
#             print(d1D)
#             print(e1D)
#             print(f1D)
#             print(g1D)
#             print(h1D)
#             print(i1D)
#             print(j1D)
#
#             print(fn_Motor1D(b1D,c1D,d1D,e1D,f1D,g1D,h1D,i1D,j1D))
#             sleep(2)
#             sleep(5)
#     for index, row in df2D.iterrows():
#             b2D=(row['CompName'])
#             c2D=(row['FwdCmd'])
#             d2D=(row['RevCmd'])
#             e2D=(row['FwdRunFb'])
#             f2D=(row['RevRunFb'])
#             g2D=(row['HealthyFb'])
#             h2D=(row['ReadyFb'])
#             i2D=(row['MCCBOnFb'])
#             j2D=(row['OverloadFb'])
#             k2D=(row['FaultFb'])
#             l2D=(row['DelayTime'])
#             print(b2D)
#             print(c2D)
#             print(d2D)
#             print(e2D)
#             print(f2D)
#             print(g2D)
#             print(h2D)
#             print(i2D)
#             print(j2D)
#
#             print(fn_Motor1D(b2D,c2D,d2D,e2D,f2D,g2D,h2D,i2D,j2D))
#             sleep(2)
#
#     for index, row in dfcv.iterrows():
#             bcv=(row['CompName'])
#             ccv=(row['SP'])
#             dcv=(row['PV'])
#             ecv=(row['DelayTime'])
#             print(bcv)
#             print(ccv)
#             print(dcv)
#             print(ecv)
#
#             print(fn_ControlValves(bcv,ccv,dcv,ecv))
#             sleep(4)
#
#     for index, row in dfat.iterrows():
#             batx=(row['CompName'])
#             catx=(row['HighLim'])
#             datx=(row['LowLim'])
#             eatx=(row['Val'])
#             fatx=(row['SelVal'])
#             gatx=(row['OutAna'])
#             print(batx)
#             print(catx)
#             print(datx)
#             print(eatx)
#             print(fatx)
#             print(gatx)
#
#             print(fn_AnalogTx(batx,catx,datx,eatx,fatx,gatx))
#             sleep(10)
# '''
#









            
