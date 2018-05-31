init python:

    class Console(object):

        def __init__(self):
            self.drag = None

        def set_frame(self, frame):
            self.text = Text("")
            self.viewport = Viewport(self.text, mousewheel=True, pos=(frame.left, frame.top), xysize=(800 - frame.left - frame.right, 480 - frame.top - frame.bottom))
            self.drag = Drag(Fixed(
                frame,
                self.viewport,
                xmaximum=800, ymaximum=480
            ))

        def show(self, layer, zorder):
            self.viewport.yoffset = 1.0
            renpy.scene_lists().add(layer, self.drag, zorder=zorder)

        def add_text(self, text):
            # set_text does some processing which I'll utilize
            old_text = self.text.text
            self.text.set_text(text)

            self.text.set_text(old_text + self.text.text)

        def set_text(self, text):
            self.text.set_text(text)


    _c = Console()


    def console_init(frame=Frame("frame-old.png", 10, 10)):
        _c.set_frame(frame)

    def console_show(layer=None, zorder=sys.maxsize):
        if not layer:
            layer = renpy.config.layers[len(renpy.config.layers)-1]
        _c.show(layer, zorder)

    def console_add_text(text):
        _c.add_text(text)

    def console_set_text(text):
        _c.set_text(text)
