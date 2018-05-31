init python:
    console_init()

label start:

    scene bg room
    show eileen happy

    "We need to investigate! Who should we send, and where should they go?"

    python:
        console_show()
        for i in range(1, 10):
            console_add_text("Monika {}\n".format(i))

    "Okay, we'll send detective to city."
