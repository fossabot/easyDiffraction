from PySide2.QtCore import Signal, QThread
import sys

class Refiner(QThread):
    """
    Simple wrapper for calling a function in separate thread
    """
    failed = Signal(str)
    finished = Signal(dict)
    message = Signal(str)

    def __init__(self, obj, method_name, parent=None):
        QThread.__init__(self, parent)
        self._obj = obj
        self.method_name = method_name
        self.previous = None
        self.current = None

    def run(self):
        sys.stdout = self
        res = {}
        if hasattr(self._obj, self.method_name):
            func = getattr(self._obj, self.method_name)
            try:
                res = func()
            except Exception as ex:
                self.failed.emit(str(ex))
                return str(ex)
        self.finished.emit(res)
        return res

    def write(self, text):
        split = text.split('     ')
        if split[0] == text:
            return
        self.previous = self.current
        try:
            self.current = [float(x) for x in split[1:]]
        except ValueError:
            return
        text = None
        if self.previous is not None:
            text = '{0:.3f}'.format(sum([((x-y)/y)**2 for x, y in zip(self.previous, self.current)])**0.5)
        self.message.emit(text)