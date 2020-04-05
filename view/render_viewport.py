from vtk import vtkActor, vtkDataSetMapper, vtkDICOMImageReader,vtkRenderer, vtkMetaImageReader, vtkRenderWindowInteractor, vtkImageViewer2
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class RenderViewport(QVTKRenderWindowInteractor):
    def __init__(self, main_window, render_data_service):
        super().__init__(main_window)
        main_window.setCentralWidget(self)
        self.renderer = vtkRenderer()
        self.renderer.AddVolume(render_data_service.volume)
        self.GetRenderWindow().AddRenderer(self.renderer)

        self.render_data_service = render_data_service
        self.render_data_service.volume_data_changed.connect(self.__update_volume)
        self.render_data_service.skin_opacity_changed.connect(self.__render)
        self.render_data_service.skin_color_changed.connect(self.__render)
        self.render_data_service.bone_color_changed.connect(self.__render)
        self.render_data_service.shading_changed.connect(self.__render)
        self.render_data_service.gradient_opactity_changed.connect(self.__render)
        
        self.renderer.GetActiveCamera().SetViewUp(0, 0, -1)
        self.renderer.GetActiveCamera().Azimuth(30.0)
        self.renderer.GetActiveCamera().Elevation(30.0)
        
        self.Initialize()
        self.Start()
        self.show()

    def __update_volume(self):
        volume_centre = self.render_data_service.volume.GetCenter()
        self.renderer.GetActiveCamera().SetPosition(volume_centre[0], volume_centre[1] - 400, volume_centre[2])
        self.renderer.GetActiveCamera().SetFocalPoint(volume_centre[0], volume_centre[1], volume_centre[2])

    def __render(self):
        self.GetRenderWindow().Render()
