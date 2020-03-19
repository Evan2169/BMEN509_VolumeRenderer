from PyQt5.QtWidgets import QDockWidget, QFileDialog, QHBoxLayout, QGroupBox, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt5.QtCore import QDir, Qt

class DockWidgetMenu(QDockWidget):
    def __init__(self, main_window):
        super().__init__("Tools", main_window)
        main_window.addDockWidget(Qt.RightDockWidgetArea, self)
        self.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.__setupInternalContents()
        self.show()

    def __setupInternalContents(self):
        layout = QVBoxLayout()
        widget = QWidget(self)

        self.__create_file_selection_view(layout, widget)

        widget.setLayout(layout)
        self.setWidget(widget)

    def __create_file_selection_view(self, layout, parent):
        file_selection_groupbox = QGroupBox("File Selection", parent)
        filename_widget = QLabel("No File Selected", file_selection_groupbox)
        open_file_button = QPushButton("Open", file_selection_groupbox)
        file_selection_layout = QHBoxLayout()
        file_selection_layout.addWidget(filename_widget)
        file_selection_layout.addWidget(open_file_button)
        file_selection_groupbox.setLayout(file_selection_layout)
        layout.addWidget(file_selection_groupbox)

        def open_file():
            file, _ = QFileDialog.getOpenFileName(parent, directory = QDir.currentPath())
            if(file):
                path_delimited = file.split("/")
                file_name_path_removed = path_delimited[len(path_delimited) - 1] 
                filename_widget.setText(file_name_path_removed)
        open_file_button.clicked.connect(open_file)
