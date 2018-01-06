import inspect
import sys
import threading
import time
import traceback
from time import strftime


class Writer:
    """

    """
    Print_Only = 0
    Write_Only = 1
    Print_Write = 2

    def __init__(self, option, file_name=None):
        self.option = option
        self.file_name = file_name
        self._file_write = self.option == Writer.Write_Only or self.option == Writer.Print_Write
        self._console_write = self.option == Writer.Print_Only or self.option == Writer.Print_Write
        self.threads = threading.enumerate()

        if self._file_write:
            with open(self.file_name, "w") as _:
                pass

    def write(self, text, nwline=True):
        if self._file_write:
            with open(self.file_name, "w+") as f:
                f.write(text)
                if nwline:
                    f.write("\n")

        if self._console_write:
            print(text)

    def write_python_information(self):
        self.write("Executable is %s" % sys.executable)
        self.write("Version is %s" % sys.version)

    def write_thread_information(self):
        t = threading.enumerate()
        self.write("Total threads are %d" % len(t))

    def print_thread_identity(self, id):
        for t in self.threads:
            if t.ident == id:
                self.write("%s(%d) daemon(%d)" % (t.name, t.ident, t.daemon))
                break

    def write_frames_information(self):

        self.write("Current frame information")

        cf = inspect.currentframe()
        traceback.print_stack(cf)
        for thread, frame in sys._current_frames().items():
            self.print_thread_identity(thread)
            traceback.print_stack(frame)

    def dump(self):
        self.write("____________________Stack dump of python_________________")
        self.write("Date: %s" % strftime("%Y-%m-%d-%H-%M-%S", time.localtime()))

        self.write_python_information()
        self.write_thread_information()
        self.write_frames_information()


if __name__ == '__main__':
    w = Writer(Writer.Print_Only)
    w.dump()
