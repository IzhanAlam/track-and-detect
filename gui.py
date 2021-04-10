from PyQt5 import uic
from PyQt5.QtWidgets import QApplication


class qtWindow():

    Form, Window = uic.loadUiType("app_gui.ui")

    app = QApplication([])
    window = Window()
    form = Form()
    form.setupUi(window)
    window.show()
    app.exec_()



