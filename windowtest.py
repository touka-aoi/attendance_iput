import sys

# For Sample
from PySide2.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QTableView
)


class TestWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.root_widget: QWidget = QWidget()
        self.layout: QVBoxLayout = QVBoxLayout()

        self.table: QTableView = QTableView()

        self.layout.addWidget(self.table)
        self.root_widget.setLayout(self.layout)

        self.setCentralWidget(self.root_widget)
        self.setWindowTitle('Test of QTableView')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()

    sys.exit(app.exec_())