# MIT License

# Copyright (c) 2018 Abdülhamit Yilmaz

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


init -2147483648 python:
    import pygame_sdl2 as pygame


    class ConsoleDrag(renpy.display.dragdrop.Drag):

        def __init__(self, event_handler, **properties):
            super(ConsoleDrag, self).__init__(**properties)
            self.event_handler = event_handler

        def event(self, ev, x, y, st):
            super(ConsoleDrag, self).event(ev, x, y, st)
            self.event_handler(ev, x, y, st)


    class ConsoleCommand(object):

        def help(self):
            return ""

        def autofill(self, argv):
            pass

        def call(self, argv):
            pass


    class _ConsoleCommandClear(ConsoleCommand):

        def __init__(self, set_text):
            self.set_text = set_text

        def help(self):
            return ("clear", "Clears the console.")

        def call(self, argv):
            self.set_text([])


    class _ConsoleCommandHelp(ConsoleCommand):

        def __init__(self, console):
            self.console = console

        def help(self):
            return ("help", "Shows this help.")

        def call(self, argv):
            for command in self.console.commands.itervalues():
                h = command.help()
                if h:
                    if hasattr(h, "__iter__"):
                        indent = ""
                        for t in h:
                            self.console._out(indent + t, True)
                            indent = "    "
                    else:
                        self.console._out(h, True)


    class Console(object):

        def __init__(self, frame=Frame("frame.png", 3, 3), shell_symbol="> ", history_limit=100, caret="|"):
            self.commands = {
                "clear": _ConsoleCommandClear(self._set_text),
                "help": _ConsoleCommandHelp(self),
            }
            self.caret = caret
            self.caret_pos = 0
            self.shown = False
            self.layer = None
            self.history_limit = history_limit
            self.drag = None
            self.shell_symbol = shell_symbol
            self.text = Text([shell_symbol, caret])
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
            texts = self.text.text[:]
            map_event = renpy.display.behavior.map_event
            last_line_index = len(texts) - 1
            last_line = texts[last_line_index]

            if map_event(ev, "input_backspace"):
                if self.caret_pos > 0:
                    texts[last_line_index] = last_line[:self.caret_pos - 1] + last_line[self.caret_pos:]
                    self.caret_pos -= 1

            if map_event(ev, "input_delete"):
                if self.caret_pos < len(last_line) - 1:
                    texts[last_line_index] = last_line[:self.caret_pos + 1] + last_line[self.caret_pos + 2:]

            elif map_event(ev, "input_home"):
                texts[last_line_index] = self.caret + last_line[:self.caret_pos] + last_line[self.caret_pos + 1:]
                self.caret_pos = 0

            elif map_event(ev, "input_end"):
                texts[last_line_index] = last_line[:self.caret_pos] + last_line[self.caret_pos + 1:] + self.caret
                self.caret_pos = len(last_line) - 1

            if map_event(ev, "input_left"):
                if self.caret_pos > 0:
                    texts[last_line_index] = last_line[:self.caret_pos - 1] + self.caret + last_line[self.caret_pos - 1] + last_line[self.caret_pos + 1:]
                    self.caret_pos -= 1

            if map_event(ev, "input_right"):
                if self.caret_pos < len(last_line) - 1:
                    texts[last_line_index] = last_line[:self.caret_pos] + last_line[self.caret_pos + 1] + self.caret + last_line[self.caret_pos + 2:]
                    self.caret_pos += 1

            elif map_event(ev, "input_enter"):
                self.call_command("\n", False, False)
                raise renpy.display.core.IgnoreEvent()

            elif ev.type == pygame.TEXTINPUT:
                texts[last_line_index] = last_line[:self.caret_pos] + ev.text + last_line[self.caret_pos:]
                self.caret_pos += 1

            elif ev.type == pygame.KEYDOWN:
                if ev.unicode and ord(ev.unicode[0]) >= 32:
                    texts[last_line_index] = last_line[:self.caret_pos] + ev.unicode + last_line[self.caret_pos:]
                    self.caret_pos += 1

            elif ev.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                self.hide()
                raise renpy.display.core.IgnoreEvent()

            else:
                return

            self.text.set_text(texts)
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

        def _set_text(self, texts):
            texts = texts[-self.history_limit:]
            self.text.set_text(texts)
            self.viewport.yoffset = 1.0

        def call_command(self, text, line_break=True, clear_line=True):
            if line_break and text[len(text) - 1] != "\n":
                text += "\n"
            texts = self.text.text[:]
            last_line_index = len(texts) - 1

            if clear_line:
                texts[last_line_index] = text
            else:
                texts[last_line_index] += text
                texts[last_line_index] = texts[last_line_index][:self.caret_pos] + texts[last_line_index][self.caret_pos + 1:]

            self._set_text(texts)

            argv = texts[last_line_index].split()
            if len(argv) > 0:
                command = self.commands.get(argv[0])
                if command:
                    command.call(argv)
                    texts = self.text.text[:]
                else:
                    texts.append("Error: Command '{}' not found.\n".format(argv[0]))

            texts.append(self.shell_symbol)
            texts.append(self.caret)
            self.caret_pos = 0

            self._set_text(texts)

        def _out(self, text, line_break=False):
            if line_break and text[len(text) - 1] != "\n":
                text += "\n"
            texts = self.text.text[:]

            texts.append(text)

            self._set_text(texts)

        def add_command(self, name, command):
            if not isinstance(name, unicode):
                raise TypeError("'name' has be of type 'unicode'")
            if not isinstance(command, ConsoleCommand):
                raise TypeError("'command' has be of type 'ConsoleCommand'")
            command.out = self._out
            self.commands[name] = command
