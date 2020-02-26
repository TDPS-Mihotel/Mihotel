# Mihotel

Mihotel项目文档

---
目录
1. [✔️得分项](#️得分项)
2. [⚠️注意事项](#️注意事项)
3. [坑](#坑)
   1. [传感](#传感)
4. [项目内容](#项目内容)
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
---

## ✔️得分项

- 实现全部要求
- 答辩和报告格式, 排版正确美观
- 答辩, 报告注意内容组织, 可能按模块分割后需要分软硬件讨论
- PPT和报告内容直观, 可以多一些图表图示

## ⚠️注意事项

- 易损元件购买时注意考虑购买备件
- 注意项目进度跟进
- 注意到第八周项目应基本成型. 因为**要给期中考试留出复习时间**, 要避让11-13周 (甚至可能更早), 而第十五周就需要提交demo视频了, 因此第八周过后只有大致**三周**时间了.
- 后期注意小组间沟通, 衔接
- 注意多团建😏

## 坑

### 传感

- patio底下埋有金属水管, 地磁传感器受干扰大
- 图像识别受光线, 地面湿润度影响大
  - 光线不足导致曝光不足, 光线太强烈导致过曝
  - 怀疑是因为如果之前下过雨地面颜色发生变化导致

## 项目内容

项目为在东湖边两个露台展开的各三个任务. 下面简称露台1, 2的一系列任务为**p1**, **p2**.

### 现场展示

现场展示一个patio的过程.

### 答辩

答辩由`30分钟PPT` (p1p2内容都要包含, **demo视频时间算在这30分钟里**) 和`10分钟Q&A`组成

💡 30分钟看似很多, 但之前有些组是每个人都说几句所以讲到了**四十多分钟** (超时一些不要紧)

💡 demo视频视角完全由我们决定, 因此完全可以有遥控完成, 出错了就剪辑等操作

❗️ 虽然demo视频只需要一个, 但在答辩前几天才会知道抽中了哪个patio, 建议两个都做. (视频时间建议2-3min)

![](doc/donghu.png)

- 下列图示中`绿条`为一个任务的起始点
- `红条`为一个任务的终止点
- `粗绿条`和`粗红条`分别为一个patio的起始点和终止点
- `紫色标号`为一些小车需按顺序经过的点

💡 每个patio可以设置至多**两个**信标. 虽然问上一届信标本身没什么限制 (即可以考虑自制GPS), 建议用标定板做信标.

### Patio 1

![](doc/patio1.png)

#### Task 1

![](doc/p1t1.png)

由`标号1`自主走到`标号6`

#### Task 2

![](doc/p1t23.png)

在`标号7`处右转过小木桥, 木桥左边界 (照片视角) 对其对面台阶右边界.  `标号7`处考虑设置一个信标.

❗️ 木桥较窄 (约**0.45m**)而长 (约**2.2m**), 上桥前如果不调整好进入角度很有可能**中途掉落**.

#### Task 3

小车下桥后在遇到的第二条轨迹处 (`标号8`) 左转, 通过过牌坊. `信标8`处考虑设置一个信标.

### Patio 2

![](doc/patio2.png)

#### Task 1

![](doc/p2t1.png)

从起始点走到`标号1`, 识别此处的提示色块, 然后到达同色色块处.

💡 色块共有红, 绿, 蓝三种颜色.

#### Task 2

![](doc/p2t2.png)

从任务1结束点以不违背总体要求的方式移动到斜槽处(`标号2`). 此处考虑使用两个信标或者利用花坛和水池. 然后将一开始携带的鱼食想法子弄到斜槽上.

❗️ `标号2`是这面栏杆从右数第二个这样的洞.

#### Task 3

到达`紫条`处, 发送包含以下信息的443MHz射频信号:

- 队名
- 队伍编号
- 当前时间 (24小时制)

❗️ 我后来确认了一下不是蓝牙信号, 但也只需要一个HC-12射频模块就可以了.

等待确认收到信息后继续前进到达`粗红条`处. (下图花坛处)

![](doc/p2t3.png)