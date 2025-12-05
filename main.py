#!/usr/bin/env python3
import sys
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel

class GPUSwitcher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GPU Switcher")
        self.resize(400, 200)

        layout = QVBoxLayout()
        self.realtime_label = QLabel("Loading...")
        self.reboot_label = QLabel("")
        layout.addWidget(self.realtime_label)
        layout.addWidget(self.reboot_label)

        btn_integrated = QPushButton("Integrated")
        btn_integrated.clicked.connect(lambda: self.switch_gpu("integrated"))
        layout.addWidget(btn_integrated)

        btn_hybrid = QPushButton("Hybrid")
        btn_hybrid.clicked.connect(lambda: self.switch_gpu("hybrid"))
        layout.addWidget(btn_hybrid)
        
        btn_refresh = QPushButton("Refresh Status")
        btn_refresh.clicked.connect(self.read_gpu_info)
        layout.addWidget(btn_refresh)
        
        self.read_gpu_info()

        self.setLayout(layout)

    def switch_gpu(self, mode):
        try:
            subprocess.run(["pkexec", "envycontrol", "-s", mode], check=True)
            
            self.read_gpu_info()
            self.reboot_label.setText("Switch successful! Reboot required.")
        except subprocess.CalledProcessError as e:
            error = e.stderr.decode().strip() if e.stderr else "Failed"
            self.reboot_label.setText(f"Failed: {error}")
        except FileNotFoundError:
            self.reboot_label.setText("envycontrol not installed!")
        
    def read_gpu_info(self):
        try:
            result = subprocess.run(
                ["envycontrol", "-q"],
                capture_output=True,
                text=True,
                check=True
            )
    
            current_mode = result.stdout.strip()
            print(current_mode)
            self.realtime_label.setText(f"Current mode: {current_mode}")
        except subprocess.CalledProcessError as e:
            self.reboot_label.setText(f"Error:\n{e.stderr or e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPUSwitcher()
    window.show()
    sys.exit(app.exec())
