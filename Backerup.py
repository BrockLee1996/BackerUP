import sys
import os
import shutil
class Get():
	def ParentDir(Path):
		Path = Path.split("\\")
		ParentDir = len(Path)-1
		return Path[ParentDir]
class Copy():
	def ParentDir(Path,ParentDir):
		os.chdir(Path) # Destination
		try:
			os.mkdir(ParentDir)
		except: FileExistsError
		return os.path.join(Path,ParentDir)
	def Run(Source,Destin):
		shutil.copytree(Source,Destin,symlinks=False,dirs_exist_ok=True)
class Main():
	def __init__(self,Source,Destin):
		self.Source = Source		
		self.Destin = Copy.ParentDir(Destin,Get.ParentDir(Source))
		print(self.Source)
		print(self.Destin)
		Copy.Run(self.Source,self.Destin)

Main(sys.argv[1],sys.argv[2])