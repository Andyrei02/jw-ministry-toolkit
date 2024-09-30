import sys
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QHBoxLayout, QWidget, QFrame, QScrollArea, QPushButton, QLabel, QComboBox
from PyQt5.QtCore import Qt

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Main layout (top-level layout)
        self.mainLayout = QVBoxLayout(self)

        # Add button
        self.addButton = QPushButton("Add Row")
        self.addButton.clicked.connect(self.add_row)
        self.mainLayout.addWidget(self.addButton)

        # Create a container layout for the fixed left frame and the scrollable right frame
        containerLayout = QHBoxLayout()

        # Left frame (fixed, will not scroll)
        self.leftFrame = QFrame()
        self.leftLayout = QVBoxLayout(self.leftFrame)
        self.leftLayout.setAlignment(Qt.AlignTop)  # Align left frame to the top

        # Add left frame to the container layout
        containerLayout.addWidget(self.leftFrame)

        # --- Create a scrollable right frame ---
        self.scrollArea = QScrollArea()
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # Disable horizontal scrolling

        # Create a right frame that will be scrollable inside the scroll area
        self.rightFrame = QFrame()
        self.rightLayout = QVBoxLayout(self.rightFrame)

        # Add the right frame to the scroll area
        self.scrollArea.setWidget(self.rightFrame)

        # Add the scroll area (right frame) to the container layout
        containerLayout.addWidget(self.scrollArea)

        # Add the container layout to the main layout
        self.mainLayout.addLayout(containerLayout)

        # Add a few initial rows
        self.row_count = 0
        self.add_row()  # Add an initial row

    def add_row(self):
        # Increment row counter
        self.row_count += 1

        # --- Left Frame: Create a new label ---
        label = QLabel(f"Name {self.row_count}")
        self.leftLayout.addWidget(label)

        # --- Right Frame: Create a row of 5 combo boxes ---
        comboBoxRowLayout = QHBoxLayout()
        for i in range(5):
            comboBox = QComboBox()
            comboBox.addItems([f"Option {i+1}", f"Option {i+2}", f"Option {i+3}"])
            comboBoxRowLayout.addWidget(comboBox)
        
        # Add the row of combo boxes to the right layout
        self.rightLayout.addLayout(comboBoxRowLayout)

        # Adjust layout size to ensure new items fit
        self.rightFrame.adjustSize()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("QFrame with Scroll Area")
    window.setGeometry(100, 100, 800, 400)
    window.show()
    sys.exit(app.exec_())

