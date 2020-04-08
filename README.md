# Mihotel

Mihotel project document.

---
Table of Contents
1. [✔️ Highlights](#️-Highlights)
2. [⚠️ Precautions](#️-Precautions)
3. [Issues](#Issues)
   1. [Sensor](#Sensor)
4. [Configurations](#Configurations)
5. [Personnel Division](#Personnel-Division)
6. [项目内容](#项目内容)
   1. [现场展示](#现场展示)
   2. [答辩](#答辩)
   3. [Patio 1](#Patio-1)
      1. [Task 1](#Task-1)
      2. [Task 2](#Task-2)
      3. [Task 3](#Task-3)
   4. [Patio 2](#Patio-2)
      1. [Task 1](#Task-1-1)
      2. [Task 2](#Task-2-1)
      3. [Task 3](#Task-3-1)
7. [报销流程及要求](#报销流程及要求)
8. [支出信息公开](#支出信息公开)

---

## ✔️ Highlights

- Fulfill all requirements
- good and fancy format of slides and report
- notice content organization of slides and report, may need to discuss the
  content by hardware and software even if in a module
- Slides and report should be intuitive, beautiful, clear tables and schematic
  diagram are welcome

## ⚠️ Precautions

- Consider purchasing spare parts when buying vulnerable components
- focus on project progress
- we should get most design done until week 9. Because we **need to leave time
  for mid-term review**, we need to avoid week 11-13 (or even earlier). However
  demo video is needed in week 15, which means there's only 2 weeks left after
  week 9...
- be care of team communication and convergence
- need more hang outs😏

## Issues

### Sensor

- there's metro pipe under the patio, geomagnetic sensor is greatly interfered
- image identification is affected much by light, ground wetness
  - insufficient light causes underexposure, too much light causes overexposure
  - color change of ground caused by rain may affect this

## Configurations

Configurations on our Raspberry Pi

| Item   | Argument        | Notes |
| ------ | --------------- | ----- |
| System | Raspbian Buster |       |
| Python | 3.7.3           |       |
| OpenCV | 4.1.0.25        |       |

📑 [details config scripts](config/README.md)

## Personnel Division

A regular automatic system development looks like this👇

![](doc/regular_development.svg)

But since **we don't have much experience** and **we don't have very long time**, we do it like this👇, start from the two green circles **at the same time.**

![](doc/our_development.svg)

- Tech Lead: [宋铸恒](https://github.com/LeoJhonSong)
  - [Chassis](https://github.com/orgs/TDPS-Mihotel/teams/chassis): [王灏天](https://github.com/Howard2503) [王子建](https://github.com/Prince-JIAN) [史超凡](https://github.com/allensted)
  - [Electrical](https://github.com/orgs/TDPS-Mihotel/teams/electrical)
    - [System Architecture](https://github.com/orgs/TDPS-Mihotel/teams/system): [宋铸恒](https://github.com/LeoJhonSong) [许瀚鹏](https://github.com/Laince20)
    - [Visual](https://github.com/orgs/TDPS-Mihotel/teams/visual): [文博](https://github.com/wb05025) [树畅](https://github.com/shuchang) [韩浩然](https://github.com/HandAdam)
    - [Decision](https://github.com/orgs/TDPS-Mihotel/teams/decision): [王子建](https://github.com/Prince-JIAN) [许瀚鹏](https://github.com/Laince20)
    - [Sensors and Peripheral Units](https://github.com/orgs/TDPS-Mihotel/teams/sensor): [韩浩然](https://github.com/HandAdam) [文博](https://github.com/wb05025)
  - [Document](https://github.com/orgs/TDPS-Mihotel/teams/document)
    - Slides: [熊汇雨](Xiong-Huiyu)
    - Demo Video: [王灏天](https://github.com/Howard2503)
    - Report: [树畅](https://github.com/shuchang) [熊汇雨](Xiong-Huiyu)
  - [Project Manager](https://github.com/orgs/TDPS-Mihotel/teams/project-manager): [褚进炜](https://github.com/LiamBishop)

📑 [detail](doc/division.md)

## 项目内容

项目为在东湖边两个露台展开的各三个任务. 下面简称露台1, 2的一系列任务为**p1**, **p2**.

### 现场展示

现场展示一个patio的过程.

### 答辩

答辩由`30分钟PPT` (p1p2内容都要包含, **demo视频时间算在这30分钟里**) 和`10分钟Q&A`组成

💡 30分钟看似很多, 但之前有些组是每个人都说几句所以讲到了**四十多分钟** (超时一些不要紧)

💡 demo视频视角完全由我们决定, 因此完全可以有遥控完成, 出错了就剪辑等操作

❗️ 虽然demo视频只需要一个, 但在答辩前几天才会知道抽中了哪个patio, 建议两个都做. (视频时间建议2-3min)

![](doc/project_content/donghu.png)

- 下列图示中`绿条`为一个任务的起始点
- `红条`为一个任务的终止点
- `粗绿条`和`粗红条`分别为一个patio的起始点和终止点
- `紫色标号`为一些小车需按顺序经过的点

💡 每个patio可以设置至多**两个**信标. 虽然问上一届信标本身没什么限制 (即可以考虑自制GPS), 建议用标定板做信标.

### Patio 1

![](doc/project_content/patio1.png)

#### Task 1

![](doc/project_content/p1t1.png)

由`标号1`自主走到`标号6`

#### Task 2

![](doc/project_content/p1t23.png)

在`标号7`处右转过小木桥, 木桥左边界 (照片视角) 对其对面台阶右边界.  `标号7`处考虑设置一个信标.

❗️ 木桥较窄 (约**0.45m**)而长 (约**2.2m**), 上桥前如果不调整好进入角度很有可能**中途掉落**.

#### Task 3

小车下桥后在遇到的第二条轨迹处 (`标号8`) 左转, 通过牌坊. `信标8`处考虑设置一个信标.

### Patio 2

![](doc/project_content/patio2.png)

#### Task 1

![](doc/project_content/p2t1.png)

从起始点走到`标号1`, 识别此处的提示色块, 然后到达同色色块处.

💡 色块共有红, 绿, 蓝三种颜色.

#### Task 2

![](doc/project_content/p2t2.png)

从任务1结束点以不违背总体要求的方式移动到斜槽处(`标号2`). 此处考虑使用两个信标或者利用花坛和水池. 然后将一开始携带的鱼食想法子弄到斜槽上.

❗️ `标号2`是这面栏杆从右数第二个这样的洞.

#### Task 3

到达`紫条`处, 发送包含以下信息的443MHz射频信号:

- 队名
- 队伍编号
- 当前时间 (24小时制)

❗️ 我后来确认了一下不是蓝牙信号, 但也只需要一个HC-12射频模块就可以了.

等待确认收到信息后继续前进到达`粗红条`处. (下图花坛处)

![](doc/project_content/p2t3.png)

## 报销流程及要求

学院对于本课程采取**凭发票报账报销政策**，需组员在购买过程中按照学院要求开具**增值税发票**.

具体报账要求详见 📑[**报账.md**](doc/报账.md)

## 支出信息公开

本栏目每周更新一次, 旨在进行**项目支出信息公开**.

具体支出明细详见 📑[**信息公开.md**](doc/信息公开.md)
