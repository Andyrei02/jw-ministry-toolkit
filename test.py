import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QProgressBar, QPushButton
from PyQt5.QtCore import Qt, QTimer, QSize

class ProgressBarDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Indeterminate ProgressBar Example")
        self.setGeometry(100, 100, 300, 150)

        layout = QVBoxLayout()

        self.progressBar = QProgressBar(self)
        self.progressBar.setStyleSheet("""
    QProgressBar {
        border: 2px solid grey;
        border-radius: 5px;
        text-align: center;
    }
    QProgressBar::chunk {
        background-color: #00FF00;
    }
""")

        self.progressBar.setAlignment(Qt.AlignCenter)
        self.progressBar.setRange(0, 0)  # Indeterminate mode
        self.progressBar.setMaximumHeight(10)
        layout.addWidget(self.progressBar)

        self.button = QPushButton("Start", self)
        self.button.clicked.connect(self.startProgress)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def startProgress(self):
        self.progressBar.setRange(0, 0)  # Indeterminate mode
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateProgress)
        self.timer.start(100)  # Update every 100 ms

    def updateProgress(self):
        # No need to update the progress bar value in indeterminate mode
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    demo = ProgressBarDemo()
    demo.show()
    sys.exit(app.exec_())
