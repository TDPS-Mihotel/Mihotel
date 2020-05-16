# install.sh说明

用途说明见该脚本注释.

## OpenCV

- 为什么指定OpenCV版本: 默认的最新版目前还有问题, 容易出现**undefined symbol: __atomic_fetch_add8**的报错. 🔗参见[这里](https://www.pyimagesearch.com/2018/09/19/pip-install-opencv/) (需要在页面手动搜索一下这个报错)
- 为什么是本地安装: 因为我尝试了许多次pip在线安装opencv, 但是网速基本为0, 因此我们采用**手动下载wheel文件并本地使用wheel文件安装**的方式安装opencv. 效果与`pip install opencv-contrib-python==4.1.0.25`没有区别, 因为这条命令只比本地安装多了一步下载.

❗️ 在运行该脚本前需要下载[opencv-contrib-python-4.1.0.25](https://www.piwheels.org/simple/opencv-contrib-python/opencv_contrib_python-4.1.0.25-cp37-cp37m-linux_armv7l.whl)并将这个文件传到树莓派的`~/Desktop`, 也就是桌面上. 这个操作可以通过VNC的文件传输来完成.

### 验证OpenCV安装

在命令行输入

```shell
python -c "import cv2; print(cv2.__version__)"
```

应当打印出OpenCV的版本号`4.1.0`

💡 在确认成功安装后wheel文件就可以删掉了.

## wiringPi

目前rpi4b源里的wiringPi版本不够新, 无法识别rpi4的gpio, 需要手动更新. 详情见[wiringPi updated to 2.52 for the Raspberry Pi 4B](http://wiringpi.com/wiringpi-updated-to-2-52-for-the-raspberry-pi-4b/)