import os
import subprocess
import sys
import time

#upload the .inp file to winSCP
def run_inp_bat(process):
    #upload
    path1 = 'batch\\UploadSCP.bat'
    result1 = subprocess.run(path1,shell=True,text=True, capture_output=True)

    #check if the file is in required location
    path2 = 'batch\\checkinpstatus.bat'
    while True:
        result2 = subprocess.run(path2,shell=True,text=True, capture_output=True)
        if result2.returncode == 0:
            print ("Submit", process,".inp file completed successfully.")
            break
        else:
            print ("Submit", process,f".inp file not detected. Retry after 30second")
            time.sleep(30)
    return

#transfer the run command to TSUBAME through Tera Term VT
def sumbit_ssh(process):
    path = 'batch\\ssh2login.bat'
    result = subprocess.run(path, shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        print("Submit job", process,"to TSUBAME completed successfully.")
    else:
        print("Submit job", process,f"to TSUBAME completed with errors. Return code: {result.returncode}")
    return

#refresh and check whether the Job-1.mdl exist or not
def check_status(process):
    #check the existense of the job-1.mdl file every 30s
    path = 'batch\\checkjobstatus.bat'
    #check if the calcualtion start
    while True:
        result1 = subprocess.run(path, shell=True, text=True, capture_output=True)
        if result1.returncode == 0:
            print("Job Calculation Start")
            break
        else:
            print("Waiting For Job Calculation Start")
            time.sleep(20)

    #wait for 30 seconds to check the exist of the Job-1.mdl. if not exist, job is done.
    time.sleep(30)
    while True:
        result2 = subprocess.run(path, shell=True, text=True, capture_output=True)
        if result2.returncode ==1 :
            print("Job Calculation finished")
            break
        else:
            print("Job is running, automatically refresh in 30seconds")
            time.sleep(30)
    return

#download the .odb file from winSCP to local
def download_file(process):
    path = 'batch\\DownloadSCP.bat'
    result = subprocess.run(path,shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        print("Download",process,"odb file to local drive completed successfully.")
    else:
        print("Download",process,f"odb file not successful. Return code: {result.returncode}")
    return

#delect the file on the remote sever
def delect_file(process):
    path = 'batch\\delecfile.bat'
    result = subprocess.run(path,shell=True, text=True, capture_output=True)
    if result.returncode == 0:
        print("Old file in remote server delected successfully")
    else:
        print("Cannot delected old file in remote server")
    return


def read_Odb():
    result = subprocess.call(["batch\\readODB.bat"])
    return

# patch all function above together (Use this in the main file!)
def Calculation(process):
    run_inp_bat(process)
    sumbit_ssh(process)
    check_status(process)
    download_file(process)
    delect_file(process)
    read_Odb()
    return

#process = "reflection"
#Calculation(process)
