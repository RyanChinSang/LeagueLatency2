import subprocess
import os

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rsrc_rc.py')


def delete():
    global file_path
    p1 = subprocess.Popen(["del", file_path],
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=True,
                          creationflags=0x08000000)
    return p1.wait()


def gen():
    if os.path.exists(file_path):
        delete()
    else:
        pass
    p1 = subprocess.Popen(["pyrcc4", "-o", "rsrc_rc.py", "rsrc.qrc"],
                          stdout=subprocess.PIPE,
                          stdin=subprocess.PIPE,
                          stderr=subprocess.PIPE,
                          shell=False,
                          creationflags=0x08000000)
    return p1.wait()
