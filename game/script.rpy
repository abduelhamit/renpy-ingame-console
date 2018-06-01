init python:
    console = Console()

label start:

    scene bg room
    show eileen happy

    "We need to investigate! Who should we send, and where should they go?"

    python:
        console.show()
        for i in range(10):
            console.add_command("Monika {}\n".format(i))
        for i in range(10, 20):
            console.add_command("Monika {}".format(i))

    "Okay, we'll send detective to city."
