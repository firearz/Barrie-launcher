import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QComboBox, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QTimer
from launcher import get_available_versions, launch_minecraft

class MinecraftLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Barrie Launcher v3.5")
        self.setWindowIcon(QIcon("icon.ico"))
        self.setFixedSize(460, 460)
        self.setStyleSheet("""
            QWidget {
                background-color: #1e1e1e;
                color: white;
                font-family: 'Segoe UI', sans-serif;
                font-size: 13px;
            }
            QLineEdit, QComboBox {
                background-color: #2c2c2c;
                border: 1px solid #3a3a3a;
                border-radius: 6px;
                padding: 8px;
                color: white;
            }
            QPushButton {
                background-color: #00C853;
                color: white;
                padding: 10px;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00e676;
            }
            QLabel {
                margin-top: 10px;
                font-weight: bold;
            }
            QProgressBar {
                border: 1px solid #444;
                border-radius: 5px;
                background-color: #2e2e2e;
                height: 20px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #00C853;
                width: 10px;
                margin: 1px;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(30, 30, 30, 30)

        # Title
        title = QLabel("🧱 Barrie Minecraft Launcher")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 22px; color: #ffffff;")
        layout.addWidget(title)

        # Username
        layout.addWidget(QLabel("👤 Username"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your Minecraft username")
        layout.addWidget(self.username_input)

        # Version
        layout.addWidget(QLabel("📦 Minecraft Version"))
        self.version_dropdown = QComboBox()
        self.version_map = {}  # Maps display name to version id
        for label, version_id in get_available_versions():
            self.version_dropdown.addItem(label)
            self.version_map[label] = version_id
        layout.addWidget(self.version_dropdown)

        # Upload skin
        self.upload_skin_btn = QPushButton("🎨 Upload Custom Skin")
        self.upload_skin_btn.setStyleSheet("background-color: #555;")
        self.upload_skin_btn.clicked.connect(self.upload_skin)
        layout.addWidget(self.upload_skin_btn)

        # Progress Bar (initially hidden)
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # Launch
        self.launch_btn = QPushButton("🚀 Launch Minecraft")
        self.launch_btn.clicked.connect(self.start_loading)
        layout.addWidget(self.launch_btn)

        # Footer
        footer = QLabel("🔧 Created by @nextgenmilo | For educational use only")
        footer.setStyleSheet("color: #888; font-size: 11px; margin-top: 20px;")
        footer.setAlignment(Qt.AlignCenter)
        layout.addWidget(footer)

        self.setLayout(layout)

    def start_loading(self):
        username = self.username_input.text()
        selected_label = self.version_dropdown.currentText()
        version = self.version_map.get(selected_label)

        if not username:
            QMessageBox.warning(self, "Missing Username", "Please enter a username.")
            return

        # Disable button and show progress bar
        self.launch_btn.setEnabled(False)
        self.progress_bar.show()
        self.progress = 0
        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self.update_progress(username, version))
        self.timer.start(50)  # Speed of progress

    def update_progress(self, username, version):
        self.progress += 2
        self.progress_bar.setValue(self.progress)

        if self.progress >= 100:
            self.timer.stop()
            try:
                self.close()
                launch_minecraft(username, version)
            except Exception as e:
                QMessageBox.critical(self, "Launch Error", f"Failed to launch Minecraft:\n{e}")

    def upload_skin(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Minecraft Skin", "", "PNG Files (*.png)")
        if file_path:
            username = self.username_input.text() or "default"
            save_path = os.path.join("barrie_skins", f"{username}.png")
            try:
                os.makedirs("barrie_skins", exist_ok=True)
                with open(file_path, 'rb') as src, open(save_path, 'wb') as dst:
                    dst.write(src.read())
                QMessageBox.information(self, "Skin Uploaded", "Skin uploaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Skin Error", f"Could not upload skin: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MinecraftLauncher()
    window.show()
    sys.exit(app.exec_())