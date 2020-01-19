import os 
import sys
from MyModules import BackEndGUI
from PyQt5.QtWidgets import*
global sourcefile
global destinationfile
from PyQt5.QtCore import*
global sourcepath
global destinationpath
global HourFreq	
HourFreq = None
sourcepath = None 
destinationpath = None 
app = QApplication([])
class Model(QDirModel): # This class defines a Directory viewing model 
	def __init__(self): # Initilize thie object 
		super(Model, self).__init__() #Give it supa powers
		self.sourceview = QTreeView() # Establish the view class for the desitnation file views 
		self.destinview = QTreeView() # Establish the view class for the destination file views 
		self.MyWindow = Window() # Creating the Layout for the file viewers 
		self.BackupName = Window()
		self.BackupName.setWindowTitle("Enter BackupName")
		self.BackupName.hide()
		self.TextInput = QLineEdit()
		#self.BackupLayout = QVBoxLayout()
		#self.BackupLayout.addWidget(self.TextInput)
		#self.BackupName.setLayout(self.BackupLayout)
		self.MyWindow.setWindowTitle("Backup Menu") 
		self.GridLayout = QGridLayout() # Views will go from left to right
		
		
		# BackUpFrequency Layout created:
		self.FrequencyLayout = QVBoxLayout() 
		self.FrequencyLabel = QLabel()
		self.FrequencyButton1 = QRadioButton("Every Hour")
		self.FrequencyButton6 = QRadioButton("Every 6 Hours")
		self.FrequencyButton24 = QRadioButton("Every 24 Hours")
		self.ButtonGroup = QButtonGroup() # ButtonGroup Allows each radio button to be exclusive in selection, meaning you can only toggle ONE 
		self.ButtonGroup.addButton(self.FrequencyButton1)
		self.ButtonGroup.addButton(self.FrequencyButton6)
		self.ButtonGroup.addButton(self.FrequencyButton24)
		self.FrequencyLabel.setFrameStyle(QFrame.WinPanel | QFrame.Raised) # Create Label with a framestyle 
		self.FrequencyLabel.setText("Backup Frequency") 
		self.FrequencyLayout.addWidget(self.FrequencyLabel) # 
		self.FrequencyLayout.addWidget(self.FrequencyButton1)
		self.FrequencyLayout.addWidget(self.FrequencyButton6)
		self.FrequencyLayout.addWidget(self.FrequencyButton24)
		self.GridLayout.addLayout(self.FrequencyLayout,3,1) # Add the Vertical Layout in Row 3, Column 1
		# Action Buttons Created 
		self.ActionButtonLayout = QVBoxLayout()
		self.SaveButton = QPushButton("Save")
		self.HelpButton = QPushButton("Help")
		self.ActionButtonLayout.addWidget(self.SaveButton)
		self.ActionButtonLayout.addWidget(self.HelpButton)
		self.GridLayout.addLayout(self.ActionButtonLayout,3,0) # Add the Vertical Layout in Row 3, Column 0
		# Source and Destination Labels above the file explorers created 
		self.SourceLabel = QLabel() # Initilizes a QLabel Object 
		self.DestinLabel = QLabel() 
		self.SourceLabel.setFrameStyle(QFrame.WinPanel | QFrame.Raised) #Creates Label style 
		self.DestinLabel.setFrameStyle(QFrame.WinPanel | QFrame.Raised)
		self.SourceLabel.setText("Source File Selection") # Text for label to be displayed 
		self.DestinLabel.setText("Destination File Selection") 
		self.GridLayout.addWidget(self.SourceLabel,1,0) #Add the source label to row 1, Column 0
		self.GridLayout.addWidget(self.DestinLabel,1,1) # Add the Destination Label row 1, Column 1
		self.GridLayout.addWidget(self.sourceview,2,0) # Add Source view to Row 2, Column 0
		self.GridLayout.addWidget(self.destinview,2,1) # Add Destination view to Row 2 coloumn 1
		self.MyWindow.setLayout(self.GridLayout) # Set the layout for the window widget 

		self.Time = self.FrequencyButton1.clicked.connect(self.Intervals) #The self.Time attribute calls the self.Intervals method when a Frequency Button is detected as being Clicked 
		self.Time = self.FrequencyButton6.clicked.connect(self.Intervals)
		self.Time = self.FrequencyButton24.clicked.connect(self.Intervals)
		
		self.sourcefile = self.sourceview.clicked.connect(self.GetSource) # When an item from the SORUCE treeview is clicked, goto the function inside
		self.destinationfile = self.destinview.clicked.connect(self.GetDestin) 
		self.CommenceBackup = self.SaveButton.clicked.connect(self.VerifyBackup) # When the SaveButton is clicked, goto the Activate Backup Method to determine if everything is valid
		self.sourceview.setModel(self) # Establish view as the view for the QDirModel Object 
		self.destinview.setModel(self)
		

		self.sourceview.setSortingEnabled(True)
		self.destinview.setSortingEnabled(True)
		print(self.sourcefile)
	def GetSource(self, index): # The index holds whatever we clicked on
		self.sourceview.clicked.disconnect(), self.sourceview.clicked.connect(self.GetSource)
		clickedsourcepath = self.fileInfo(index).absoluteFilePath() #Index that is clicked will get the file info and absoulte path leading to that index 
		while clickedsourcepath == self.fileInfo(index).absoluteFilePath(): # When the user clicks on a file in the tree, the absoulte file path of whatever they clicked will be stored
			confirmbox = QMessageBox.question(QMainWindow(), "Source Selection", "You have selected\n" + clickedsourcepath + "\n Is this your source file that you wish to create a backup of?",   # Message Box requring user input 
			QMessageBox.Yes | QMessageBox.No )
			if confirmbox & QMessageBox.No: # If this is NOT what they want, then return to the selection of the source path 
				return self.sourceview.clicked.disconnect(), self.sourceview.clicked.connect(self.GetSource) # Disconnect the signal then reconnect it after the user clicks on what they want
			if confirmbox & QMessageBox.Yes: # If this IS what they want, return the clickedsourcepath as the true sourcepath 
				global sourcepath # Global Sourcepath will be used to pass to the BackEndGUI module which will store both of them 
				sourcepath = clickedsourcepath  # Define the value 
				sourcepath = sourcepath.replace("/","\\")
				print(sourcepath)
				return sourcepath, BackEndGUI.aquire_Source(sourcepath) # Return both the sourcepath and the return value of the backend result 
				break
				
	def GetDestin(self, index):
		self.destinview.clicked.disconnect(), self.destinview.clicked.connect(self.GetDestin)
		clickeddestinpath = self.fileInfo(index).absoluteFilePath()
		while clickeddestinpath == self.fileInfo(index).absoluteFilePath():
			confirmbox = QMessageBox.question(QMainWindow(), "Destination Selection", "You have selected\n" + clickeddestinpath + "\n Is this your destination file that you wish to create a backup in?",   # Message Box requring user input 
			QMessageBox.Yes | QMessageBox.No )
			if confirmbox & QMessageBox.No: # If this is NOT what they want, then return to the selection of the source path 
				return self.destinview.clicked.disconnect(), self.destinview.clicked.connect(self.GetDestin)
			if confirmbox & QMessageBox.Yes: # If this IS what they want, return the clickedsourcepath as the true sourcepath 
				global destinationpath
				destinationpath = clickeddestinpath
				destinationpath = destinationpath.replace("/", "\\")
				#The aquire both method from the BackEndGUI will put them both together in the same scope from which actions will be taken 
				return destinationpath, BackEndGUI.aquire_Destin(destinationpath) #BackEndGUI.aquire_both(BackEndGUI.aquire_Source(sourcepath),BackEndGUI.aquire_Destin(destinationpath)) 
				break 
	def VerifyBackup(self): # This method will confirm and push forward the backup solution


		if BackEndGUI.aquire_Source(sourcepath) == None: # If NO SourceSelection has been done
			confirmbox = QMessageBox.warning(QMainWindow(), "Warning", "You have not selected a SOURCE file yet!",
				QMessageBox.Ok | QMessageBox.Help)
			if confirmbox & QMessageBox.Ok:
				return
			if confirmbox & QMessageBox.Help: # Will present a window detailing use of software 
				QMessageBox.information(self.MyWindow,"Help","blah blah blah blah")


		if BackEndGUI.aquire_Destin(destinationpath) == None:
			confirmbox = QMessageBox.warning(QMainWindow(), "Warning", "You have not selected a DESTINATION file yet!",
				QMessageBox.Ok | QMessageBox.Help)
			if confirmbox & QMessageBox.Ok:
				return
			if confirmbox & QMessageBox.Help:
				QMessageBox.information(self.MyWindow,"Help","The right file table is for the destinaiton. Please select one and click yes to confirm it")


		if HourFreq	 == None:
			confirmbox	= QMessageBox.warning(QMainWindow(),"Warning", "You have not selected a TIME INTERVAL yet!",
				QMessageBox.Ok	| QMessageBox.Help)
			if confirmbox & QMessageBox.Ok:
				return
			if confirmbox & QMessageBox.Help:
				QMessageBox.information(self.MyWindow,"Help","In the bottom right of the menu, are the time interval options, please select one")


		if BackEndGUI.aquire_Source(sourcepath) and BackEndGUI.aquire_Destin(destinationpath) != None and HourFreq	 != None:
			confirmbox = QMessageBox.question(self.MyWindow, "Commence Backup", sourcepath + " is going to be saved into the destination: " + destinationpath + " Every " + str(HourFreq)  + " Hour/s"
				"\n                    Continue?", QMessageBox.Yes | QMessageBox.No )
			if confirmbox & QMessageBox.Yes:
				#self.BackupName.show()
				BackupNameBox, okPressed = QInputDialog.getText(self.MyWindow, "Backup", "Name of Backup Process:", QLineEdit.Normal, "")
				if okPressed and BackupNameBox != "":
					BackEndGUI.aquire_both(sourcepath,destinationpath,HourFreq,BackupNameBox,os.getcwd()) # Pass the source and destination to the backend

				if okPressed and BackupNameBox == "":
					confirmbox	= QMessageBox.warning(QMainWindow(),"Warning", "You have not entered a BACKUP NAME yet!",
						QMessageBox.Ok	| QMessageBox.Help)
				
			if confirmbox & QMessageBox.No:
				return

	def Intervals(self): # Passes the hour to the backend to be converted to minutes for backend functions 		 
		global HourFreq	#The global variable HourFreq is used to hold the Hour frequency and will be used to provide feedback to user
		if self.FrequencyButton1.isChecked() == True: # If the 1 hour button is checked:
				HourFreq = 1 # HourFreq is set to 1 to represent 1 hour # For testing purposes in command prompt 
				#return BackEndGUI.Interval(1)	 # Convert hour to minute in the backend 
		if self.FrequencyButton6.isChecked() == True:
				#global HourFreq
				HourFreq = 6	
				#return BackEndGUI.Interval(6)	
		if self.FrequencyButton24.isChecked() == True:
				#global HourFreq
				HourFreq = 24
				#return BackEndGUI.Interval(24)		
		
		

		
class Window(QWidget): 
	def __init__(self):
		super(Window, self).__init__()

		





## All this will execute First
M = Model()
M.MyWindow.show() # Show the layout with all the component
app.exec_()
