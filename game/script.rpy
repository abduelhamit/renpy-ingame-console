init python:
    console = Console()

label start:

    scene bg room
    show eileen happy

    "We need to investigate! Who should we send, and where should they go?"

    python:
        console.show()
        class Test(ConsoleCommand):
            def call(self, argv):
                self.out(str(argv), True)
        # for i in range(10):
        #     console.add_command("Monika {}\n".format(i))
        # for i in range(10, 20):
        #     console.add_command("Monika {}".format(i))
        console.add_command("bla", Test())

    "Okay, we'll send detective to city."
    "Test"

    python:
        console.show()

    "And again"
