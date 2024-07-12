from PyQt5.QtWidgets import *
import sys
from gui import App 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())