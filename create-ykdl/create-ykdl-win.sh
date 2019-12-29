#!/bin/sh

HERE="$(dirname "$(readlink -f "${0}")")"

# Download latest ykdl code
if [ -d ykdl ]; then
    rm -rf ykdl
fi
git clone 'https://github.com/zhangn1985/ykdl.git'

# Run PyInstaller
cp "${HERE}/ykdl_main.py" ykdl/ykdl-moonplayer.py
cd ykdl
pyinstaller -F --additional-hooks-dir hooks --distpath .. ykdl-moonplayer.py
cd ..
