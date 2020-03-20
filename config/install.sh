#! /bin/bash
# ------------------------------------------------------------------------------
# Install essential softwares and packages.
#
# To descrease download speed apt source and Raspbian source are changed to
# tsinghua. Another side effect is that default pip and python are changed to
# pip3 and python3.
#
# ❗Notice that you should download the spefified opencv-contrib-python wheel
# file to **Desktop** before executing it. (you can get download link in README)
# ------------------------------------------------------------------------------

# backup apt source list and Raspbian source list and change them to tsinghua mirror
sudo cp /etc/apt/sources.list /etc/apt/sources.list.bak
sudo cp /etc/apt/sources.list.d/raspi.list /etc/apt/sources.list.d/raspi.list.bak
sudo sh -c 'echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib" > /etc/apt/sources.list'
sudo sh -c 'echo "deb-src http://mirrors.tuna.tsinghua.edu.cn/raspbian/raspbian/ buster main non-free contrib" >> /etc/apt/sources.list'
sudo sh -c 'echo "deb http://mirrors.tuna.tsinghua.edu.cn/raspberrypi/ buster main ui" > /etc/apt/sources.list.d/raspi.list'
sudo apt update

# remove the soft links to pip2 and python2
sudo rm /usr/bin/pip
sudo rm /usr/bin/python
# then install update-alternatives
sudo update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# change to tsinghua pip mirror and upgrade pip
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip install pip -U

# install OpenCV and its dependencies
sudo apt-get install -y libhdf5-dev libhdf5-103
sudo apt-get install -y libqtgui4 libqtwebkit4 libqt4-test python3-pyqt5
sudo apt-get install -y libatlas-base-dev
sudo apt-get install -y libjasper-dev
pip install ~/Desktop/opencv_contrib_python-4.1.0.25-cp37-cp37m-linux_armv7l.whl  # ❗this wheel file has to be there first
