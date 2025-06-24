import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon('public/ttrack_app_icon.svg'))
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())