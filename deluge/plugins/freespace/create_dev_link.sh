#!/bin/bash
cd /home/vampas/projects/DelugeNotify/deluge/plugins/freespace
mkdir temp
export PYTHONPATH=./temp
python setup.py build develop --install-dir ./temp
cp ./temp/FreeSpace.egg-link .config/plugins
rm -fr ./temp
