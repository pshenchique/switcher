# Basic python

``` bash
python -m venv venv
source venv/bin/activate
pip install pyside6
```

# Compile

``` bash
pip install nutika
python -m nuitka --onefile --enable-plugin=pyside6 --output-dir=/tmp main.py
 cp /tmp/main.bin ~/switcher
chmod +x gpu-switcher
sudo mv gpu-switcher /usr/local/bin/
```

# Desktop settings:

``` bash
cat > ~/.local/share/applications/gpu-switcher.desktop << 'EOF'
[Desktop Entry]
Encoding=UTF-8
Name=GPU Switcher
Comment=Switch between Integrated and Hybrid GPU modes
Exec=/usr/local/bin/gpu-switcher
Icon=video-display
Terminal=false
Type=Application
Categories=Utility;
EOF
```