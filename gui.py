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




qtWindow()




confidence_threshold = qtWindow.form.doubleSpinBox.value()
sensitive_confidence_threshold = qtWindow.form.doubleSpinBox_2.value()
maxDetectFail = qtWindow.form.spinBox_4.value()
detection_interval = qtWindow.form.spinBox_3.value()
slower_detection = qtWindow.form.checkBox_4.isChecked()

maxTrackFail = qtWindow.form.spinBox_5.value()
duplicate_object_threshold = qtWindow.form.doubleSpinBox_3.value()
show_poly = qtWindow.form.checkBox.isChecked()
poly_outside = qtWindow.form.checkBox_3.isChecked()
set_obj_range = qtWindow.form.checkBox_2.isChecked()





print(confidence_threshold,sensitive_confidence_threshold, maxDetectFail,
detection_interval, slower_detection, maxTrackFail, duplicate_object_threshold,
show_poly, poly_outside, set_obj_range)
