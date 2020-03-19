from vtk import vtkRenderer
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class RenderViewport(QVTKRenderWindowInteractor):
    def __init__(self, main_window):
        super().__init__(main_window)
        main_window.setCentralWidget(self)
        self.renderer = vtkRenderer()
        self.GetRenderWindow().AddRenderer(self.renderer)
        self.show()
        self.GetRenderWindow().GetInteractor().Initialize()
        self.GetRenderWindow().GetInteractor().Start()
