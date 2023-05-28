from abaqus import *
from abaqusConstants import *
from odbAccess import openOdb
from textRepr import *
from numpy import array
from numpy import genfromtxt
import numpy as np
import time
import __main__
import os
import os.path
import sys
import xlwt

#locate file path
odb = openOdb('abafiles\\result\\Job-1.odb')
assembly = odb.rootAssembly
Target_node = assembly.instances['PART-1-1'].nodeSets['NODE9']
#Target_node = part['PART-1'].nodeSets['NODE9']

#define target node
elementL = 1
Target_element = assembly.instances['PART-1-1'].getElementFromLabel(label = elementL)

#define time and frames
times = []
Stress = []
step1 = odb.steps['Step-1']
frames = step1.frames

#define the property of model
radius = 0.0025

i = 0
j = 0
k = 0

#create new excel file
wbk1 = xlwt.Workbook()
sheet = wbk1.add_sheet('sheet1')

#extract data from each frame
for frame in frames:
    times.append(frame.frameValue)
    displacement = frame.fieldOutputs['U']
    stress = frame.fieldOutputs['S']
    node_disp = displacement.getSubset(region=Target_node)
    ele_stress = stress.getSubset(region = Target_element)

    #calculate reaction force
    #displacement in diameter
    radius_disp = node_disp.values[0].data[0]
    longti_disp = float(node_disp.values[0].data[1]) #convert to float
    current_radius =  radius - radius_disp
    cross_area = current_radius**2*3.1415926
    S33 = ele_stress.values[0].mises

    Stress.append(ele_stress.values[0].mises)

    #print (longti_disp, S33)


#Output displacement and stress to excel
    sheet.write(i,0,current_radius)
    sheet.write(i,1,longti_disp)
    sheet.write(i,2,S33)
    i += 1
wbk1.save('Job-1.xls')

odb.close()


#read data and Nelder Mead Simplex method


'''
    #for vv in node_stress.values:
    #Displacement.append(node_disp.values[0])

'''