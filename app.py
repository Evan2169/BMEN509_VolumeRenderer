from PyQt5.QtWidgets import QApplication, QMainWindow
from sys import exit

from view.view_container import ViewContainer

def run():
    app = QApplication([])
    window = QMainWindow()
    
    views = ViewContainer(window)

    window.show()
    app.processEvents()
    exit(app.exec_())

if __name__ == "__main__":
    run()
