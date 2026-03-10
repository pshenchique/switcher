import sys
import subprocess
import shutil
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
            self._run_envycontrol(["pkexec", "envycontrol", "-s", mode])
            
            self.read_gpu_info()
            self.reboot_label.setText("Switch successful! Reboot required.")
        except subprocess.CalledProcessError as e:
            error = self._format_envycontrol_error(e)
            self.reboot_label.setText(f"Failed: {error}")
        except FileNotFoundError:
            self.reboot_label.setText("envycontrol not installed!")
        
    def read_gpu_info(self):
        if shutil.which("envycontrol") is None:
            self.realtime_label.setText("Current mode: unknown")
            self.reboot_label.setText("envycontrol is not available in PATH")
            return

        try:
            result = self._run_envycontrol(["envycontrol", "-q"])
    
            current_mode = result.stdout.strip()
            self.realtime_label.setText(f"Current mode: {current_mode}")
        except subprocess.CalledProcessError as e:
            self.realtime_label.setText("Current mode: unknown")
            self.reboot_label.setText(f"Error:\n{self._format_envycontrol_error(e)}")

    def _run_envycontrol(self, command):
        return subprocess.run(command, capture_output=True, text=True, check=True)

    def _format_envycontrol_error(self, error):
        details = (error.stderr or error.stdout or "").strip()

        if "PackageNotFoundError" in details:
            return (
                "envycontrol is installed incorrectly (missing Python package metadata). "
                "Reinstall it with your distro package manager or pip."
            )

        if not details:
            return str(error)

        return details.splitlines()[-1]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GPUSwitcher()
    window.show()
    sys.exit(app.exec())
