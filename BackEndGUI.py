import os 
import subprocess
import shutil
import sys
import threading
def aquire_Source(SourcePath):
	
	S = SourcePath
	return S
def aquire_Destin(DestinPath):
	
	D = DestinPath
	return D


def aquire_both(S,D,Time,BackupSaveName,Path): # This method will get passed the source, destination, and time interval
	ConfigName = BackupSaveName
	Min = Time * 60
	CreateBatch(S,D,Min,BackupSaveName,Path)
def CreateBatch(S,D,Time,BackupSaveName,Path):
	BatHandler = open(BackupSaveName + ".bat", "w")
	FileName = BackupSaveName + ".bat"
	WriteToBatch(S,D,Time,BatHandler,Path)
	MoveToBatchFolder(FileName,Time)
	#os.system("Backupthread.py" + BackupSaveName)
def WriteToBatch(S,D,Time,BatchFile,Path):
	BatchFile.write(Path + "\\" + "Backerup.py" + " " + S + " " + D )
	BatchFile.close()
def MoveToBatchFolder(FileName,Time):
	print("Moving to Batch Folder.....")
	if os.path.exists(os.getcwd() + "\\BatchFolder") is False:
		os.mkdir("BatchFolder")
		shutil.move(FileName,os.getcwd() + "\\BatchFolder")
	else:
		shutil.move(FileName, os.getcwd() + "\\BatchFolder")
	os.chdir(os.getcwd() + "\\BatchFolder")
	WaitThread(FileName,Time)
def WaitThread(FileName,Time):
	RunThread = threading.Timer(Time,StartThread,[FileName])
	RunThread.start()
def StartThread(FileName):
	subprocess.call(FileName)
	WaitThread(FileName,Time)













