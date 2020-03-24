from PyQt5.QtWidgets import QDockWidget, QFileDialog, QHBoxLayout, QGroupBox, QLabel, QPushButton, QSlider, QVBoxLayout, QWidget
from PyQt5.QtCore import QDir, Qt
import vtk

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
        self.__sharpening_filter(layout, widget)
        self.__gaussian_filter(layout, widget)

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

    def __sharpening_filter(self, layout, parent):

        sharpening_groupbox = QGroupBox("Sharpening Filter", parent)
        sharpen_label = QLabel("Sharpen", sharpening_groupbox)
        sharpen_slider = QSlider(Qt.Horizontal)
        sharpen_slider.setMinimum(0)
        sharpen_slider.setMaximum(2000)
        sharpen_slider.setValue(1000)

        #sharpen_slider.valueChanged.connect(self.sharpen)

        sharpen_layout = QHBoxLayout()
        sharpen_layout.addWidget(sharpen_label)
        sharpen_layout.addWidget(sharpen_slider)
        sharpening_groupbox.setLayout(sharpen_layout)
        layout.addWidget(sharpening_groupbox)

    def __gaussian_filter(self, layout, parent):

        gaussian_groupbox = QGroupBox("Gaussian Filter", parent)
        gaussian_radius_label = QLabel("Radius Factor", gaussian_groupbox)
        gaussian_radius_slider = QSlider(Qt.Horizontal)
        gaussian_radius_slider.setMinimum(0)
        gaussian_radius_slider.setMaximum(2000)
        gaussian_radius_slider.setValue(1000)

        gaussian_std_label = QLabel("Standard Dev.", gaussian_groupbox)
        gaussian_std_slider = QSlider(Qt.Horizontal)
        gaussian_std_slider.setMinimum(0)
        gaussian_std_slider.setMaximum(2000)
        gaussian_std_slider.setValue(1000)

        gaussian_layout = QHBoxLayout()
        gaussian_layout.addWidget(gaussian_radius_label)
        gaussian_layout.addWidget(gaussian_radius_slider)

        gaussian_layout.addWidget(gaussian_std_label)
        gaussian_layout.addWidget(gaussian_std_slider)

        gaussian_groupbox.setLayout(gaussian_layout)
        layout.addWidget(gaussian_groupbox)

        '''
        gaussian = vtk.vtkImageGaussianSmooth()
        gaussian.SetStandardDeviation(2)
        gaussian.SetDimensionality(3)
        gaussian.SetRadiusFactor(1)
        gaussian.SetInput(imageIn.GetOutput())
        gaussian.Update()
        '''
        #vtkImageGaussianSmooth
        #vtkImageMedian3D
