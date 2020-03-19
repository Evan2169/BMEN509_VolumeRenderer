from view.dock_widget_menu import DockWidgetMenu
from view.render_viewport import RenderViewport

class ViewContainer():
    def __init__(self, main_window):
        self.dock_widget_menu = DockWidgetMenu(main_window)
        self.render_viewport = RenderViewport(main_window)
