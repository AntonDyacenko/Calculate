from PyQt5 import Qt
import pyqtgraph as pg
import numpy as np
import Project


def is_number(str):
    try:
        float(str)
        return True
    except ValueError:
        return False


class Window(Qt.QWidget):

    def __init__(self):
        super().__init__()

        layout = Qt.QVBoxLayout(self)
        self.sp = []

        self.view = view = pg.PlotWidget()
        self.curve = view.plot(name="Line")

        self.btn = Qt.QPushButton("Добавить")
        self.inx = Qt.QLineEdit()
        self.iny = Qt.QLineEdit()
        self.btn2 = Qt.QPushButton("Калькулятор")

        layout.addWidget(self.view)
        layout.addWidget(self.btn)
        layout.addWidget(Qt.QLabel("Ведите X"))
        layout.addWidget(self.inx)
        layout.addWidget(Qt.QLabel("Ведите Y"))
        layout.addWidget(self.iny)
        layout.addWidget(self.btn2)
        self.btn.clicked.connect(self.app)
        self.btn2.clicked.connect(self.open)

    def app(self):
        if is_number(self.inx.text()) and is_number(self.iny.text()):
            self.sp.append([float(self.inx.text()), float(self.iny.text())])
        random_array = np.array(self.sp)
        self.curve.setData(random_array)

    def open(self):
        self.sss = True
        self.s = Project.FirstForm()
        self.s.show()
        self.close()


if __name__ == "__main__":
    app = Qt.QApplication([])
    w = Window()
    w.show()
    app.exec()
