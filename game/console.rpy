init python:
    class Console(object):
        def __init__(self):
            self.drag = None
        def set_frame(self, frame):
            self.drag = Drag(frame)
        def show(self, layer, zorder):
            renpy.scene_lists().add(layer, self.drag, zorder=zorder)
    _c = Console()
    def init_console(frame=Frame("frame-old.png", 10, 10, xmaximum=800, ymaximum=480)):
        _c.set_frame(frame)
    def console(layer=None, zorder=sys.maxsize):
        if not layer:
            layer = renpy.config.layers[len(renpy.config.layers)-1]
        _c.show(layer, zorder)
