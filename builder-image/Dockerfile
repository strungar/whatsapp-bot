from ubuntu:24.04

run apt update
run apt install -y wget gpg unzip
run mkdir -pm755 /etc/apt/keyrings && wget -O - https://dl.winehq.org/wine-builds/winehq.key | gpg --dearmor -o /etc/apt/keyrings/winehq-archive.key -

run dpkg --add-architecture i386
run wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/noble/winehq-noble.sources
run apt update && apt install -y --install-recommends winehq-stable && apt clean

env PYTHONHOME=/opt/python
env WINEARCH=win32
env WINEPREFIX=/.wine32
env WINEPATH=Z:\\opt\\python;Z:\\opt\\python\\Scripts;C:\\windows\\system32;C:\\windows;C:\\windows\\system32\\wbem;C:\\windows\\system32\\WindowsPowershell\\v1.0

run wget "https://www.python.org/ftp/python/3.9.5/python-3.9.5-embed-win32.zip" && unzip python-3.9.5-embed-win32.zip -d /opt/python/ && rm -f python-3.9.5-embed-win32.zip
run wget "https://bootstrap.pypa.io/get-pip.py" -O /opt/python/get-pip.py

run sed 's:#import site:import site:' -i /opt/python/python*._pth
run sed -ri 's:args.append\("pip"\):\0\n    args.append("pyinstaller")\n    args.append("virtualenv"):' /opt/python/get-pip.py

run wine python Z:\\opt\\python\\get-pip.py
copy build.bat /opt/python/Scripts/build.bat

entrypoint [ "wine", "/opt/python/Scripts/build.bat" ]
