from src.app.mainWindow import *
from PyQt5.QtWidgets import QApplication
from sys import argv as sysArgv, exit as sysExit
from os.path import dirname

if __name__ == "__main__":
    sysArgv += ['-platform', 'windows:darkmode=1']
    app = QApplication(sysArgv)
    player = MusicPlayer()
    
    with open(f"{dirname(__file__)}\\src\\assets\\css\\styles.css", 'r') as styleFile:
        player.style(styleFile.read())
    
    player.show()
    sysExit(app.exec_())