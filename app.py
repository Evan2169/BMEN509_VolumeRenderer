from PyQt5.QtWidgets import QApplication, QMainWindow
from sys import exit

from domain.domain_container import DomainContainer
from view.view_container import ViewContainer

def run():
    app = QApplication([])
    app.setApplicationName("Volume Renderer")
    window = QMainWindow()
    
    domain = DomainContainer()
    views = ViewContainer(window, domain)

    window.show()
    app.processEvents()
    exit(app.exec_())

if __name__ == "__main__":
    run()
