from enum import Enum
from PyQt5.QtCore import pyqtSignal, QObject
import vtk

class DataType(Enum):
    DICOM = 1
    META_IMAGE = 2

class RenderDataService(QObject):
    volume_data_changed = pyqtSignal()
    skin_opacity_changed = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.volume = vtk.vtkVolume()

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
        volumeScalarOpacity = vtk.vtkPiecewiseFunction()
        volumeScalarOpacity.AddPoint(0, 0.00)
        volumeScalarOpacity.AddPoint(500, percent_opaque)
        volumeScalarOpacity.AddPoint(1000, percent_opaque)
        volumeScalarOpacity.AddPoint(1150, 0.85)
        self.volume.GetProperty().SetScalarOpacity(volumeScalarOpacity)
        self.volume.Update()
        self.skin_opacity_changed.emit()

    def __setup_default_volume_parameters(self, image_reader):
            volume_mapper = vtk.vtkGPUVolumeRayCastMapper()
            volume_mapper.SetInputConnection(image_reader.GetOutputPort())

            volumeColor = vtk.vtkColorTransferFunction()
            volumeColor.AddRGBPoint(0, 0.0, 0.0, 0.0)
            volumeColor.AddRGBPoint(500, 1.0, 0.5, 0.3)
            volumeColor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
            volumeColor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

            volumeScalarOpacity = vtk.vtkPiecewiseFunction()
            volumeScalarOpacity.AddPoint(0, 0.00)
            volumeScalarOpacity.AddPoint(500, 0.15)
            volumeScalarOpacity.AddPoint(1000, 0.15)
            volumeScalarOpacity.AddPoint(1150, 0.85)

            volumeGradientOpacity = vtk.vtkPiecewiseFunction()
            volumeGradientOpacity.AddPoint(0, 0.0)
            volumeGradientOpacity.AddPoint(90, 0.5)
            volumeGradientOpacity.AddPoint(100, 1.0)

            volumeProperty = vtk.vtkVolumeProperty()
            volumeProperty.SetColor(volumeColor)
            volumeProperty.SetScalarOpacity(volumeScalarOpacity)
            volumeProperty.SetGradientOpacity(volumeGradientOpacity)
            volumeProperty.SetInterpolationTypeToLinear()
            volumeProperty.ShadeOn()
            volumeProperty.SetAmbient(0.4)
            volumeProperty.SetDiffuse(0.6)
            volumeProperty.SetSpecular(0.2)

            self.volume.SetMapper(volume_mapper)
            self.volume.SetProperty(volumeProperty)

