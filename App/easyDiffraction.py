import os
import sys

from PySide2.QtCore import QUrl, Qt, QCoreApplication
from PySide2.QtWidgets import QApplication
from PySide2.QtQml import QQmlApplicationEngine

import RhoChiQml

class MainWindow():
    def __init__(self):
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)

        self.setupApp()
        proxy = RhoChiQml.Proxy()
        self.setupEngine(proxy=proxy)

    def setupApp(self):
        self.app = QApplication(sys.argv)
        self.app.setOrganizationName("ESS")
        self.app.setOrganizationDomain("esss.se")
        self.app.setApplicationName("easyDiffraction")

    def setupEngine(self, proxy=None):
        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("proxy", proxy)

        self.engine.addImportPath(os.path.join(os.path.dirname(sys.argv[0]), "Imports"))
        self.engine.load(QUrl.fromLocalFile(os.path.join(os.path.dirname(sys.argv[0]), "Gui.qml")))

    def exec(self):
        self.app.exec_()

if __name__ == '__main__':

    main_app = MainWindow()
    if main_app.engine.rootObjects():
        sys.exit(main_app.exec())
    
