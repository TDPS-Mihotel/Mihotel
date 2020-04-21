# Mihotel

Mihotel project document.

---
Table of Contents
1. [✔️ Highlights](#️-Highlights)
2. [⚠️ Precautions](#️-Precautions)
3. [Configurations](#Configurations)
4. [🔍 Output Description](#-Output-Description)
5. [Solution (WIP)](#Solution-WIP)
   1. [System](#System)
      1. [Structure](#Structure)
      2. [Communication](#Communication)
      3. [How it ends](#How-it-ends)
   2. [Chassis](#Chassis)
   3. [Visual & Sensor](#Visual--Sensor)
   4. [Decision](#Decision)
6. [Development Strategy](#Development-Strategy)
7. [Personnel Division](#Personnel-Division)
8. [Project Specifications](#Project-Specifications)
9. [Tasks](#Tasks)
   1. [Task1](#Task1)
   2. [Task2](#Task2)
   3. [Task3](#Task3)
   4. [Task4](#Task4)
   5. [Task5](#Task5)
10. [报销流程及要求](#报销流程及要求)
11. [支出信息公开](#支出信息公开)

---

## ✔️ Highlights

- Fulfill all requirements
- good and fancy format of slides and report earns points
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
- need more hang outs 🍻

## Configurations

List of tools, modules with their version

| Item                                            | Argument      | Notes                                   |
| ----------------------------------------------- | ------------- | --------------------------------------- |
| System                                          | Webots R2020a |                                         |
| Python                                          | 3.7.3         |                                         |
| opencv-contrib-python                           | 4.2.0.32      | OpenCV module for python                |
| time                                            |               | python built-in module                  |
| multiprocessing                                 |               | python built-in module                  |
| [colorama](https://github.com/tartley/colorama) |               | python module for colored terminal text |

## 🔍 Output Description

| Style         | prefix     | Description                                                  |
| ------------- | ---------- | ------------------------------------------------------------ |
| Bright Green  | [Info]     |                                                              |
| Bright Red    | [Debug]    | debug information, the difference against info is that, this should not show up unless is debugging |
| Bright Blue   | [Command]  | command given to chassis                                     |
| Bright Yellow | [Detected] | detect of object                                             |

## Solution (WIP)

### System

#### Structure

The **system** sets up **3 processes**, one for chassis controlling, one for decision, one for detection.

![](doc/processes.svg)

#### Communication

Two queues, **signal_queue**, **command_queue** are used for communications between processes. Although it seems when there is only two endpoints to communicate, [`Pipe()` is a faster choice](https://stackoverflow.com/a/8463046/10088906), but it seems the code could be prettier with `Queue()`.

❗️ notice that once `Queue.get()` is used, one item in the queue is taken out and returned, which means **it is not in the queue anymore** and you could not get it again with `Queue.get()`.

#### How it ends

the main process ends when `flag_patio_finished` turns to **True**. Now all three child processes are set to **daemonic child process** by `Process.daemon = True`, therefore, [the child processes will be terminated as soon as the main process completes](https://stackoverflow.com/a/25391156/10088906).

📚 [document for `multiprocessing.Queue()`](https://docs.python.org/3/library/multiprocessing.html#multiprocessing.Queue)

### Chassis

The **chassis** of the rover is size of **15cm*45cm**, with wheels which diameter is **10cm**. The max speed of the rover is not decided yet. It is a **4WD** chassis, which mean speed of each wheel is separately defined.

![](doc/rover.jpg)

The **feeding device** acts like a garbage truck dumping trash, we dump the kiwi by raising one side of the kiwi holder to let the kiwi slides down.

### Visual & Sensor

Our **line detector** works like this:

1. Filtering the original picture to denoise then get the gradient distribution of the picture.
2. Cut the whole picture into N rows averagely. (N=4 in current code)
3. For each segmentation of the picture, for each the point whose magnitude of gradient is greater than the threshold (15 in current code), classify them according to the direction of their gradient. (from 1° to 360°)
4. For each segmentation of the picture, find the direction which contains the most point whose magnitude of gradient exceed the threshold.
5. Average the direction of the N segmentation and it is the direction of the eage of the path. Rotate it by 90° and we could get the direction of the path.

### Decision

The **decision making** is still working in progress at [#46](https://github.com/TDPS-Mihotel/Mihotel/issues/46)

## Development Strategy

A regular automatic system development looks like this👇

![](doc/regular_development.svg)

But since **we don't have much experience** and **we don't have very long time**, we do it like this👇, start from the two green circles **at the same time**, which saves our time and gives us more chances to adjust the design.

![](doc/our_development.svg)

## Personnel Division

- Tech Lead: [宋铸恒](https://github.com/LeoJhonSong)
- [Chassis](https://github.com/orgs/TDPS-Mihotel/teams/chassis): [王灏天](https://github.com/Howard2503) [王子建](https://github.com/Prince-JIAN) [史超凡](https://github.com/allensted)
- [Electrical](https://github.com/orgs/TDPS-Mihotel/teams/electrical)
  - [System Architecture](https://github.com/orgs/TDPS-Mihotel/teams/system): [宋铸恒](https://github.com/LeoJhonSong) [许瀚鹏](https://github.com/Laince20)
  - [Visual](https://github.com/orgs/TDPS-Mihotel/teams/visual): [文博](https://github.com/wb05025) [树畅](https://github.com/shuchang) [韩浩然](https://github.com/HandAdam)
  - [Decision](https://github.com/orgs/TDPS-Mihotel/teams/decision): [王子建](https://github.com/Prince-JIAN) [许瀚鹏](https://github.com/Laince20)
  - [Sensors and Peripheral Units](https://github.com/orgs/TDPS-Mihotel/teams/sensor): [韩浩然](https://github.com/HandAdam) [文博](https://github.com/wb05025)
- Environment: [褚进炜](https://github.com/LiamBishop) [熊汇雨](https://github.com/Xiong-Huiyu)
- [Document](https://github.com/orgs/TDPS-Mihotel/teams/document)
  - Slides: [熊汇雨](https://github.com/Xiong-Huiyu)
  - Demo Video: [王灏天](https://github.com/Howard2503)
  - Report: [树畅](https://github.com/shuchang) [熊汇雨](https://github.com/Xiong-Huiyu)
- [Project Manager](https://github.com/orgs/TDPS-Mihotel/teams/project-manager): [褚进炜](https://github.com/LiamBishop)

📑 [detail](doc/division.md)

## Project Specifications

First a homemade simulation environment, a.k.a. the patio is needed.

The required patio is shown below. Explicit labeled measurements can not be changed.

❗️ the green and red boxes are just for illustration, should not really appear.

![](doc/patio.png)

| Item   | Measurement                          |
| ------ | ------------------------------------ |
| Rover  | maximum of 50x50 cm                  |
| Bridge | 100 cm wide, 3 m long                |
| Arch   | 100 cm wide, 100 cm high (suggested) |

## Tasks

### Task1

From the start point get to the first red box following the line.

💡 although there should not really be a red box, but can be set and measured by distance.

### Task2

Release a kiwi into the pond when the orange box is detected.

### Task3

Detect the bridge and go across it, the get to the right of the trees.

💡 Here a beacon could be used to avoid tree recognition.

### Task4

Detect the arch and get through it. Then follow the line to the color box.

### Task5

recognize color of the color box and follow the line in same color to the end.

💡 Color of the color box could be set manually.

## 报销流程及要求

学院对于本课程采取**凭发票报账报销政策**，需组员在购买过程中按照学院要求开具**增值税发票**.

具体报账要求详见 📑[**报账.md**](doc/报账.md)

## 支出信息公开

本栏目每周更新一次, 旨在进行**项目支出信息公开**.

具体支出明细详见 📑[**信息公开.md**](doc/信息公开.md)
