import ctypes, sys


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    print "Hello1"
else:
    print "Hello2"
    # Re-run the program with admin rights
    ctypes.windll.shell32.ShellExecuteW(None, u"runas", unicode(sys.executable), u"", None, 1)