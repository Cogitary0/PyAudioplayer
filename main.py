from src.app.mainWindow import MainWindow
from src.utils.parse import Settings
from PyQt5.QtWidgets import QApplication
from sys import argv as sysArgv, exit as sysExit
from os.path import dirname

if __name__ == "__main__":
    
    if (Settings('config\\settings.toml').get('theme') == 'dark'):
        sysArgv += ['-platform', 'windows:darkmode=1']
        
    sysArgv += ['-platform']
    
    app = QApplication(sysArgv)
    player = MainWindow('config\\settings.toml', 'config\\language.toml')
    player.show()
    sysExit(app.exec_())
    
   