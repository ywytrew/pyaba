import os
import numpy as np
import xlwt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl
from abaqus import *
import sys
from abaqusConstants import *
import subprocess
import time

def rewriteINPfile(material_parameter):
#change the material parameter of the .inp file
    filename = "abafiles\\input\\Job-1.inp"
    #read length
    length = len(material_parameter)
    #Convert np list to string
    parameter_list = np.array2string(material_parameter,precision=None, separator=', ')
    #replace [] with blanket
    parameter_list = parameter_list.replace("[","")
    parameter_list = parameter_list.replace("]"," ")
    parameter_list = parameter_list.replace("\n"," ")
    # open .inp file
    with open(filename,"r+") as file:
        data = file.readlines()
        data[137] = parameter_list + "\n"

        file.seek(0) #let the pointer back to the intial position
        file.truncate(123) #delete the existed content of this line
        file.writelines(data) #write the data

    file.close()
