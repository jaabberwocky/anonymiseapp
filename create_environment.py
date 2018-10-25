import os


def create_environment():
    if os.path.isdir(os.path.join(os.getcwd(), "tmp")):
        pass
    else:
        os.mkdir("tmp")
    return None
