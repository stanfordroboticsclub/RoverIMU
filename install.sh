#!/usr/bin/env sh

FOLDER=$(dirname $(realpath "$0"))
cd $FOLDER

yes | sudo pip3 install quick2wire-api
sudo apt-get install -y i2c-tools

# untessted!
. raspi-config nonint
do_i2c 0

for file in *.service; do
    [ -f "$file" ] || break
    sudo ln -s $FOLDER/$file /lib/systemd/system/
done
