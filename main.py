from src.app.mainWindow import MainWindow
from PyQt5.QtWidgets import QApplication
from sys import argv as sysArgv, exit as sysExit
from os.path import dirname

if __name__ == "__main__":
    sysArgv += ['-platform', 'windows:darkmode=1']
    
    app = QApplication(sysArgv)
    player = MainWindow()
    
    player.show()
    sysExit(app.exec_())