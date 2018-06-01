init python:
    import pygame_sdl2 as pygame


    class ConsoleDrag(renpy.display.dragdrop.Drag):

        def __init__(self, event_handler, **properties):
            super(ConsoleDrag, self).__init__(**properties)
            self.event_handler = event_handler

        def event(self, ev, x, y, st):
            super(ConsoleDrag, self).event(ev, x, y, st)
            self.event_handler(ev, x, y, st)


    class Console(object):

        def __init__(self, frame=Frame("frame-old.png", 10, 10), shell_symbol="> ", history_limit=100):
            self.shown = False
            self.layer = None
            self.history_limit = history_limit
            self.drag = None
            self.shell_symbol = shell_symbol
            self.text = Text(shell_symbol)
            self.viewport = Viewport(self.text, mousewheel=True, pos=(frame.left, frame.top), xysize=(800 - frame.left - frame.right, 480 - frame.top - frame.bottom))
            self.drag = ConsoleDrag(
                self.event,
                d=Fixed(
                    frame,
                    self.viewport,
                    xmaximum=800, ymaximum=480
                )
            )

        def event(self, ev, x, y, st):
            text = self.text.text[:]
            map_event = renpy.display.behavior.map_event
            last_line = len(text) - 1

            if map_event(ev, "input_backspace"):
                if text[last_line] != "":
                    text[last_line] = text[last_line][:len(text[last_line]) - 1]

            elif map_event(ev, "input_enter"):
                self.add_command("\n", False)
                raise renpy.display.core.IgnoreEvent()

            elif ev.type == pygame.TEXTINPUT:
                text[last_line] += ev.text

            elif ev.type == pygame.KEYDOWN:
                if ev.unicode and ord(ev.unicode[0]) >= 32:
                    text[last_line] += ev.unicode

            elif ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                self.hide()
                raise renpy.display.core.IgnoreEvent()

            else:
                return

            self.text.set_text(text)
            self.viewport.yoffset = 1.0

            raise renpy.display.core.IgnoreEvent()

        def show(self, layer=None, zorder=sys.maxsize):
            if self.shown:
                return
            if not layer:
                layer = renpy.config.layers[len(renpy.config.layers) - 1]
            self.layer = layer
            self.viewport.yoffset = 1.0
            renpy.scene_lists().add(layer, self.drag, zorder=zorder)
            self.shown = True

        def hide(self):
            if not self.shown:
                return
            renpy.scene_lists().remove(self.layer, self.drag)
            self.shown = False

        def add_command(self, text, line_break=True):
            if line_break and text[len(text) - 1] != "\n":
                text += "\n"
            texts = self.text.text[:]
            texts[len(texts) - 1] += text
            texts.append(self.shell_symbol)
            texts.append("")
            texts = texts[-self.history_limit:]

            self.text.set_text(texts)
            self.viewport.yoffset = 1.0
