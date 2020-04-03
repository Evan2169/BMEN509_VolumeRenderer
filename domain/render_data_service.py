from enum import Enum
from PyQt5.QtCore import pyqtSignal, QObject
import vtk

class DataType(Enum):
    DICOM = 1
    META_IMAGE = 2


class RenderDataService(QObject):
    volume_data_changed = pyqtSignal()
    skin_opacity_changed = pyqtSignal()
    skin_color_changed = pyqtSignal()
    bone_color_changed = pyqtSignal()
    shading_changed = pyqtSignal()
    gradient_opactity_changed = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.volume = vtk.vtkVolume()
        
        self.skin_color = [255, 127.5, 76.5]
        self.bone_color = [255, 255, 229.5]
        self.skin_opacity = 0.15
        self.use_shading = True
        self.use_gradient_opacity = True

    def change_data(self, path_to_data, data_type):
        if data_type is DataType.DICOM:
            image_reader = vtk.vtkDICOMImageReader()
            image_reader.SetDirectoryName(path_to_data)
            self.__setup_default_volume_parameters(image_reader)
            self.volume_data_changed.emit()
        elif data_type is DataType.META_IMAGE:
            image_reader = vtk.vtkMetaImageReader()
            image_reader.SetFileName(path_to_data)
            self.__setup_default_volume_parameters(image_reader)
            self.volume_data_changed.emit()

    def set_skin_opacity(self, percent_opaque):
        self.skin_opacity = percent_opaque
        self.__set_scalar_opacity()
        self.skin_opacity_changed.emit()

    def set_skin_color(self, skin_color):
        self.skin_color = skin_color
        self.__set_colors()
        self.skin_color_changed.emit()

    def set_bone_color(self, bone_color):
        self.bone_color = bone_color
        self.__set_colors()
        self.bone_color_changed.emit()

    def enable_shading(self, enabled):
        self.use_shading = enabled
        self.__set_shading()
        self.shading_changed.emit()

    def enable_gradient_opacity(self, enabled):
        self.use_gradient_opacity = enabled
        self.__set_gradient_opacity()
        self.gradient_opactity_changed.emit()

    def __setup_default_volume_parameters(self, image_reader):
        volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
        volume_mapper.SetInputConnection(image_reader.GetOutputPort())

        volumeGradientOpacity = vtk.vtkPiecewiseFunction()
        volumeGradientOpacity.AddPoint(0, 0.0)
        volumeGradientOpacity.AddPoint(90, 0.5)
        volumeGradientOpacity.AddPoint(100, 1.0)

        volumeProperty = vtk.vtkVolumeProperty()
        volumeProperty.SetInterpolationTypeToLinear()
        volumeProperty.SetGradientOpacity(volumeGradientOpacity)
        volumeProperty.SetAmbient(0.4)
        volumeProperty.SetDiffuse(0.6)
        volumeProperty.SetSpecular(0.2)

        self.volume.SetMapper(volume_mapper)
        self.volume.SetProperty(volumeProperty)
        self.__set_colors()
        self.__set_scalar_opacity()
        self.__set_gradient_opacity()
        self.__set_shading()

    def __set_scalar_opacity(self):
        volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        volumeScalarOpacity.AddPoint(0, 0.00)
        volumeScalarOpacity.AddPoint(500, self.skin_opacity)
        volumeScalarOpacity.AddPoint(1000, self.skin_opacity)
        volumeScalarOpacity.AddPoint(1150, 0.85)

        self.volume.GetProperty().SetScalarOpacity(volumeScalarOpacity)
        self.volume.Update()

    def __set_colors(self):
        volumeColor = vtk.vtkColorTransferFunction()
        volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
        volumeColor.AddRGBPoint(500,  self.skin_color[0]/255, self.skin_color[1]/255, self.skin_color[2]/255)
        volumeColor.AddRGBPoint(1000, self.skin_color[0]/255, self.skin_color[1]/255, self.skin_color[2]/255)
        volumeColor.AddRGBPoint(1150, self.bone_color[0]/255, self.bone_color[1]/255, self.bone_color[2]/255)
        self.volume.GetProperty().SetColor(volumeColor)
        self.volume.Update()

    def __set_shading(self):
        if self.use_shading is True:
            self.volume.GetProperty().ShadeOn()
        else:
            self.volume.GetProperty().ShadeOff()

    def __set_gradient_opacity(self):
        if self.use_gradient_opacity is True:
            self.volume.GetProperty().DisableGradientOpacityOff()
        else:
            self.volume.GetProperty().DisableGradientOpacityOn()
