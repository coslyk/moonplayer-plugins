#!/bin/sh

HERE="$(dirname "$(readlink -f "${0}")")"

# Download latest ykdl code
if [ -d ykdl ]; then
    rm -rf ykdl
fi
git clone 'https://github.com/zhangn1985/ykdl.git'

# Copy patched file
cp "${HERE}/ykdl_main.py" ykdl/__main__.py

# Compress to zip file
cd ykdl
zip -q ../ykdl-moonplayer ykdl/*.py ykdl/*/*.py ykdl/*/*/*.py __main__.py
cd ..

# Create standalone
echo '#!/usr/bin/env python' > ykdl-moonplayer
cat ykdl-moonplayer.zip >> ykdl-moonplayer
rm ykdl-moonplayer.zip
chmod a+x ykdl-moonplayer
