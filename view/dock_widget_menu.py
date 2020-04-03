from PyQt5.QtWidgets import (
    QCheckBox, QColorDialog, QDialog,  
    QDockWidget, QFileDialog, QGroupBox, 
    QHBoxLayout, QLabel, QPushButton, 
    QSlider, QVBoxLayout, QWidget
)
from PyQt5.QtCore import QDir, Qt
import vtk

from domain.render_data_service import DataType

class DockWidgetMenu(QDockWidget):
    def __init__(self, main_window, render_data_service):
        super().__init__("Tools", main_window)
        self.render_data_service = render_data_service 
        
        main_window.addDockWidget(Qt.RightDockWidgetArea, self)
        self.setAllowedAreas(Qt.RightDockWidgetArea | Qt.LeftDockWidgetArea)
        self.__setupInternalContents()
        self.show()

    def __setupInternalContents(self):
        layout = QVBoxLayout()
        widget = QWidget(self)

        self.__create_file_selection_view(layout, widget)
        self.__create_skin_opacity_view(layout, widget)
        self.__create_volume_color_view(layout, widget)
        self.__create_toggle_misc_properties_view(layout, widget)

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
            def set_filename_and_close_dialog(path, dialog, data_type):
                if(path):
                    path_delimited = path.split("/")
                    file_name_path_removed = path_delimited[len(path_delimited) - 1]
                    filename_widget.setText(file_name_path_removed)
                    self.render_data_service.change_data(path, data_type)
                    dialog.done(QDialog.Accepted)

            def open_single_file(dialog, data_type):
                file, _ = QFileDialog.getOpenFileName(parent, directory = QDir.currentPath())
                set_filename_and_close_dialog(file, dialog, data_type)

            def open_directory(dialog, data_type):
                directory = QFileDialog.getExistingDirectory(parent, directory = QDir.currentPath())
                set_filename_and_close_dialog(directory, dialog, data_type)

            file_type_selection_dialog = QDialog(parent,  Qt.WindowTitleHint | Qt.WindowCloseButtonHint)
            file_type_selection_layout = QHBoxLayout()
            dicom_button = QPushButton("DICOM Directory", file_type_selection_dialog)
            dicom_button.clicked.connect(lambda : open_directory(file_type_selection_dialog, DataType.DICOM))
            file_type_selection_layout.addWidget(dicom_button)
            meta_image_button = QPushButton("Meta Image File", file_type_selection_dialog)
            meta_image_button.clicked.connect(lambda : open_single_file(file_type_selection_dialog, DataType.META_IMAGE))
            file_type_selection_layout.addWidget(meta_image_button)
            file_type_selection_dialog.setLayout(file_type_selection_layout)
            file_type_selection_dialog.open()

        open_file_button.clicked.connect(open_file)

    def __create_skin_opacity_view(self, layout, parent):
        skin_opacity_groupbox = QGroupBox("Toggle Skin Opacity", parent)
        skin_opacity_label = QLabel("Opacity", skin_opacity_groupbox)
        skin_opacity_slider = QSlider(Qt.Horizontal)
        skin_opacity_slider.setMinimum(0)
        skin_opacity_slider.setMaximum(100)
        skin_opacity_slider.setValue(self.render_data_service.skin_opacity * 100)
        skin_opacity_layout = QHBoxLayout()
        skin_opacity_layout.addWidget(skin_opacity_label)
        skin_opacity_layout.addWidget(skin_opacity_slider)
        skin_opacity_groupbox.setLayout(skin_opacity_layout)
        layout.addWidget(skin_opacity_groupbox)

        def change_skin_opacity(value):
            self.render_data_service.set_skin_opacity(value/100)

        skin_opacity_slider.valueChanged.connect(change_skin_opacity)

    def __create_volume_color_view(self, layout, parent):
        def color_picker_skin():
            color = QColorDialog.getColor()
            color = color.getRgb()
            self.render_data_service.set_skin_color(color)

        def color_picker_bone():
            color = QColorDialog.getColor()
            color = color.getRgb()
            self.render_data_service.set_bone_color(color)

        volume_color_groupbox = QGroupBox("Color Parameters", parent)
        skin_color_button = QPushButton("Pick Skin Color", volume_color_groupbox)
        skin_color_button.clicked.connect(color_picker_skin)
        bone_color_button = QPushButton("Pick Bone Color", volume_color_groupbox)
        bone_color_button.clicked.connect(color_picker_bone)

        volume_color_layout = QVBoxLayout()
        volume_color_layout.addWidget(skin_color_button)
        volume_color_layout.addWidget(bone_color_button)

        volume_color_groupbox.setLayout(volume_color_layout)
        layout.addWidget(volume_color_groupbox)

    def __create_toggle_misc_properties_view(self, layout, parent):
        toggle_misc_properties_groupbox = QGroupBox("Toggle Misc. Properties", parent)
        
        toggle_shading_checkbox = QCheckBox("Shading", toggle_misc_properties_groupbox)
        toggle_shading_checkbox.setCheckState(Qt.Checked if self.render_data_service.use_shading is True else Qt.Unchecked)
        def toggle_shading(state):
            self.render_data_service.enable_shading(state == Qt.Checked)
        toggle_shading_checkbox.stateChanged.connect(toggle_shading)

        toggle_gradient_opacity_checkbox = QCheckBox("Gradient Opacity", toggle_misc_properties_groupbox)
        toggle_gradient_opacity_checkbox.setCheckState(Qt.Checked if self.render_data_service.use_gradient_opacity is True else Qt.Unchecked)
        def toggle_gradient_opacity(state):
            self.render_data_service.enable_gradient_opacity(state == Qt.Checked)
        toggle_gradient_opacity_checkbox.stateChanged.connect(toggle_gradient_opacity)
        
        toggle_misc_properties_layout = QVBoxLayout()
        toggle_misc_properties_layout.addWidget(toggle_shading_checkbox)
        toggle_misc_properties_layout.addWidget(toggle_gradient_opacity_checkbox)
        toggle_misc_properties_groupbox.setLayout(toggle_misc_properties_layout)
        layout.addWidget(toggle_misc_properties_groupbox)
