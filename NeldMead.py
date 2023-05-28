import numpy as np
import xlwt
import pandas as pd
from pandas import ExcelWriter
from pandas import ExcelFile
import openpyxl
import xlrd
from Input_module import rewriteINPfile
from RMSE import RMSE_Calculate
import subprocess
import sys
from runbat import Calculation

#Read parameter from excel
i = 0 #colomn of data 行
j = 0 #row of data 列
k = 0
df1 = pd.read_excel('NelderMead.xlsx',sheet_name='Sheet1')
column = df1.values[:,0]
row = df1.values[0]
scale_column = len(column)
scale_row = len(row)

matrix = np.zeros([scale_column,scale_row]) #zero matrix for the material parameter
new_matrix = np.zeros([scale_column,scale_row]) #zero matrix for the new shrinked matrix
RSME_list = np.zeros([scale_column]) #zero matrix for the list of RMSE
W = np.zeros([scale_row]) #zero matrix for worst point
SW = np.zeros([scale_row]) #zero matrix for the second worst point
B = np.zeros([scale_row]) #zero matrix for the best point
G = np.zeros([scale_row]) #zero matrix for average point
R = np.zeros([scale_row]) #zero matrix for reflect point
E = np.zeros([scale_row]) #zero matrix for Expand point
C = np.zeros([scale_row]) #zero matrix for Contract point
CC = np.zeros([scale_row]) #zero matrix for Contract point
S = np.zeros([scale_row]) #zero matrix for Shrink point

#give values to each position
# f(1),f(2),...,f(n),f(n+1),
for colum in column:
    for ro in row:
        parameter = df1.values[i,j]
        matrix [i,j] = parameter
        j += 1
        k += 1
    j = 0
    i += 1
i = 0
print("current parameter group:",matrix)

#Read RSME value from excel
df2 = pd.read_excel('NelderMead.xlsx',sheet_name='Sheet2')
RSME_row = df2.values[:]
print(RSME_row)
for error in RSME_row:
    RSME = df2.values[i]
    RSME_list[i] = RSME
    i += 1
i = 0
print("RSME list:",RSME_list)

#iterations start
for interation in range(1,5):
    print("interation:",interation)
    # find the worst group W by obtainning its line number
    worst_index = np.argmax(RSME_list)
    print("worst_index:", worst_index)
    # Give the value to W
    for worst in row:
        W[j] = matrix[worst_index, j]
        j += 1
    j = 0
    print("worst group of parameter:", W)

    # find the best point B
    best_index = np.argmin(RSME_list)
    print("best index:", best_index)
    for best in row:
        B[j] = matrix[best_index, j]
        j += 1
    j = 0

    # find the second worst point SW
    # create new martirx by removing the worst value
    sorted_indices = np.argsort(RSME_list)
    reversed_indices = sorted_indices[::-1]
    SW_index = reversed_indices[1]
    print("Second Worst point:", SW_index)
    for second_worst in row:
        SW[i] = matrix[SW_index, i]
        i += 1
    i = 0
    print("Second Worst group parameter", SW)

    # calculate the average point G
    # calculate the average of the second column
    for C10 in row:
        G[i] = (np.sum(matrix[:, i]) - W[i]) / (scale_column - 1)
        j += 1
        i += 1
    i = 0
    j = 0
    print(G)

    # calculate the reflect point R as f(R)
    print("Doing Relfection:")
    for C10 in row:
        R[i] = 2 * G[i] - W[i]
        i += 1
    i = 0
    print(R)
    # rewrite INP file
    rewriteINPfile(R)
    # sumbit .inp file and calculate the RSME result as f(R) and wait for finish
    Calculation("reflection")
    # calculate RSME and output RSME to Excel
    RMSE_R = RMSE_Calculate(interation,"reflection")

    # if the RSME of R is between the best and worst point, accept R and replace the worst point
    if (RMSE_R < RSME_list[SW_index]) and (RMSE_R >= RSME_list[best_index]):
        matrix[worst_index] = R

        # replace the worst index in RMSE_list
        RSME_list[worst_index] = RMSE_R

    else:
        pass

    # Expand
    if (RMSE_R < RSME_list[best_index]):
        print("Doing Expansion:")
        for C10 in row:
            E[i] = G[i] + 2 * (G[i] - W[i])
            i += 1
        i = 0
        print(E)
        # sumbit E to .inp file and calculate the RSME result as f(E)
        rewriteINPfile(E)

        # submit to ABAQUS
        Calculation("Expansion")

        # calculate RMSE of E
        RMSE_E = RMSE_Calculate(interation,"Expansion")

        # if the RSME of E is smaller than R, accecpt E
        if (RMSE_E < RMSE_R):
            matrix[worst_index] = E

            # replace the RMSE_R with RMSE_E
            RSME_list[worst_index] = RMSE_E

        else:
            pass

    # Contract
    if (RMSE_R > RSME_list[SW_index]):
        if (RMSE_R < RSME_list[worst_index]):
            print("Doing Contract outside")
            for C10 in row:
                C[i] = G[i] + (R[i] - G[i]) / 2
                i += 1
            i = 0
            # submit C to .inp file
            rewriteINPfile(C)

            # submit to ABAQUS
            Calculation("Contract outside")

            # extract the result from .odb file

            # calculate the RMSE of C
            RMSE_C = RMSE_Calculate(interation,"Contract outside")

            if (RMSE_C < RMSE_R):
                matrix[worst_index] = C

                # replace R with C in RMSE_list
                RSME_list[worst_index] = RMSE_C

            else:  # do shrink
                print("Doing Shrink")
                for colum in column:
                    for ro in row:
                        new_matrix[i, j] = B[j] + (matrix[i, j] - B[j]) / 2
                        j += 1
                    j = 0
                    i += 1
                i = 0
                matrix = new_matrix
                print("new matrix", matrix)

        elif (RMSE_R > float(RSME_list[worst_index])):
            print("Doing Contract inside")
            for C10 in row:
                CC[i] = G[i] + (W[i] - G[i]) / 2
                i += 1
            i = 0
            # submit CC to .inp file
            rewriteINPfile(CC)

            # submit to ABAQUS
            Calculation("Contract inside")

            # calcualte the RMSE of CC
            RMSE_CC = RMSE_Calculate(interation,"Contract inside")

            if (RMSE_CC < float(RSME_list[worst_index])):
                matrix[worst_index] = CC

                RSME_list[worst_index] = RMSE_CC
            else:  # do shrink
                print("Doing Shrink")
                for colum in column:
                    for ro in row:
                        new_matrix[i, j] = B[j] + (matrix[i, j] - B[j]) / 2
                        j += 1
                    j = 0
                    i += 1
                i = 0
                matrix = new_matrix
                print("new matrix", matrix)


    else:  # do shrink
        print("Doing Shrink")
        for colum in column:
            for ro in row:
                new_matrix[i, j] = B[j] + (matrix[i, j] - B[j]) / 2
                j += 1
            j = 0
            i += 1
        i = 0
        matrix = new_matrix
        print("new matrix", matrix)

    #calculate the RSME of new matrix
    print("Caculating the RMSE of new matrix")
    for new_colum in column:
        rewriteINPfile(matrix[i])
        Calculation("updata newgroup")
        RSME_list[i]=RMSE_Calculate(interation,i)
        i += 1
    i = 0



    print(RSME_list)

