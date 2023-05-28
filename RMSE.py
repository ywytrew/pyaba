import numpy as np
import openpyxl
import xlwt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl
import matplotlib.pyplot as plt
import os

def RMSE_Calculate(iterations,process):

    #import experiment value
    i = 0 #row in test
    j = 0 #row in simulation
    df_test = pd.read_excel('test.xlsx',sheet_name='Sheet1')
    strain_test = []
    stress_test = []
    idx = []
    closest_simValue = []
    MSE = []

    strainT = df_test.values[:,0]
    stressT = df_test.values[:,1]

    df_sim = pd.read_excel('Job-1.xls',sheet_name='sheet1',)
    length = 0.01
    strainS = df_sim.values[:,1]/length
    stressS = df_sim.values[:,2]

    #find the same strain in test and simulation
    for strain in strainT:
        strain_test = strainT[i]
        stress_test = stressT [i]
        array = np.array(strainS)
        #find the id of the closest value
        idx = (np.abs(array-strain_test)).argmin()
        closest_strainSim = array[idx]
        closest_stressSim = stressS[idx]

        sq = ((stress_test - closest_stressSim)**2)
        MSE.append(sq)
        i += 1
    def avg(list):
        return sum(list)/len(list)

    RMSE_val = (avg(MSE))**0.5
    print(RMSE_val)

    #draw plot and save to specific path
    save_path = 'image\\'
    name = str(iterations) + '-'+ str(process)

    plt.scatter(strainT,stressT)
    plt.scatter(strainS,stressS)

    plt.xlabel('strain')
    plt.ylabel('stress')
    plt.title(name+' RMSE:'+str(RMSE_val))

    plt.savefig(save_path+name+".png")
    plt.clf()


    return RMSE_val
'''
    #output RMSE to excel
    readfile = openpyxl.load_workbook('D:\\yang\\CAE\\pythonProject\\NelderMead.xlsx')
    worksheet = readfile('Sheet3')
    worksheet.cell(row = 1, column = 1, value = RMSE_val)
'''
#Find the Avg Sqrt of the MSE

#RMSE_Calculate(1,"reflection")
