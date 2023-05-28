# pyaba
#This is a maual for the Parameter Identification tool
#The file that is not mentioned is not changeable

Package required:
#make sure your python version is beyond 3.10.8
numpy
matplotlib
pandas
openpyxl
xlwt
xlrd
scipy
pyabaqus


#the python version used in abaqus is python 2.7. Therefore you need to find coresponding patch of numpy, xlrd, xlwt for the abaqus python version.



python script(.py file)
input_module.py
    This modulue is used to edit the material parameters in the ABAQUS .inp file. 
    Before everything start, You need modify the lines in the .inp file by change the line28 code.

runbat.py
    This modulue is used to submit/read the Job.inp/Odb file to ABAQUS solver (Locally) or upload/upload the Job.inp/Odb file from the winSCP.

ODB_DispStress.py
    This modulue is used to read the displacement,stress of the node of the fieldoutput from .ODB file for each increament. You can modified it to obtain any output you want in this modulus.

RSME.py
    This modulue calculate the Root Mean Sqaure Error between experimental and simulation, the value of RSME will be used as the evaluation of Simplex algrithm. 

NelderMead.py
    This the main file of the calcualtion. After obtaining the ODB file from remote server, the RSME error is calculated by using RSME.py.
    The number of iterations is currently decided with for loop, you can modified the iteration number. 
    The detail of the method can be found in: https://jp.mathworks.com/help/optim/ug/fminsearch-algorithm.html


batch file(.bat file)
readODB.bat
    This is windows batch file that submit the .inp job to local ABAQUS solver, you can change the dirtionary of ABAQUS location path by editing it.
    After the calculation, the batch file will excute ODB_DispStress.py automatically.

UploadSCP/DownloadSCP
    upload/Download the .inp file and .ODB file to WinSCP/localfile.
    The upload/Download 
    Remember to change the path to fit the configuration you use
    more information is in: https://winscp.net/eng/docs/faq_batch_file#cmd
    command list: https://winscp.net/eng/docs/scripting#commands

ssh2login.ttl
    this file contains the login and key configuration file and sumbit script to TSUBAME
    这个文件包含登录文件和DSA密钥，以及提交给TSUBAME的命令
    More information can be found: https://webkaru.net/linux/cat/setting/ssh/
                                   https://glodia.jp/blog/11994/#コマンド投入

ssh2login.bat
    This file is used to excute ssh2login.ttl under Windows environment (linux has different method)

checkinpstatus/checkinpstatus
    These two file is to check if the job is in succuessfully upload to the sever/begin to  calculation.
    the job-1.mdl will exist during the calculation, and delected automatically after the calculation is finished

delectfile.bat
    This file is used to clear the old file in the dirtionary after download the Odb file to local. The exist old file may be possible to jam the judgement of the program
