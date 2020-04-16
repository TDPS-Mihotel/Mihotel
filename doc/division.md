<div align='right'>
  <a href='division.md'>
    <kbd>English</kbd>
  </a>
  <a href='分工.md'>
    <kbd>中文</kbd>
  </a>
</div>

## Roles Description

### Project Manager

- manage budget, in charge of reimbursement
- submit materials on behalf of team
- supervise project progress
- coordinate experiment timetable of every sub-team

### Chassis

- in charge of drive function of the chassis
- 3D model the whole rover by SolidWorks (including the chassis, sensors, fish
  food dropper and so on)
- modify the chassis to fix the mother board, sensors and so on
- design and build the fish food dropper (directly controlled by RPi or STM32 is
  to be determined)
- provide interface for RPi to communicate with STM32 by TCP/UART

### Electrical

#### System Architecture

- install and configure the Raspberry system
- configure the environment needed by other sub-teams
- synthesize modules into a system
- develop the Mihotel script for a set of command used for configuration, debug
  and execution
- configure the ssh connection settings
- configure the program as a auto start service
- add power-on music

#### Visual

- line recongnization
- orange box recongnization
- color recongnization
- (tree recongnization)

#### Decision

- route planning (work with Sensors & Peripheral Units group)
- rover behavioral decision making

#### Sensors and Peripheral Units

- in charge of beacon positioning, beacon recongnization
- figure out sensors (color sensor, ultrasonic sensor, Gyroscope sensor) sheme
  and code for them
- determine the position and angle of camera and sensors on the rover, help
  members from chassis group to draw them into the 3D model
- in charge of HC-12 RF module

### Environment

- build the webots world file to fit the specifications.

### Document

#### Slides

- in charge of Slides
- Slides materials collecting

#### Video

- in charge of demo video
- video materials collecting

#### Report

- report leading writer

## Role Will Table

| 部门 | 岗位                       |                              |                              |                             |                             |
| ---- | -------------------------- | ---------------------------- | ---------------------------- | --------------------------- | --------------------------- |
| 经理 | 经理                       | :heavy_check_mark: 褚进炜70  |                              |                             |                             |
| 底盘 | 平台改装, 驱动, 投饲料机构 | :heavy_check_mark: 王灏天100 | :heavy_check_mark: 王子建100 | 史超凡90                    | 许瀚鹏30                    |
| 电气 | 系统                       | :heavy_check_mark: 宋铸恒100 | :heavy_check_mark: 许瀚鹏90  | 褚进炜10                    |                             |
|      | 视觉                       | :heavy_check_mark: 文博90    | :heavy_check_mark: 树畅90    | :heavy_check_mark: 韩浩然80 | 熊汇雨60                    |
|      | 控制                       | :heavy_check_mark: 史超凡100 | :heavy_check_mark: 王子建80  | 韩浩然70                    | :heavy_check_mark: 许瀚鹏60 |
|      | 传感器及外围设备           | :heavy_check_mark: 韩浩然90  | 王子建80                     | :heavy_check_mark: 文博80   |                             |
| 文档 | PPT                        | 文博80                       | :heavy_check_mark: 熊汇雨60  |                             |                             |
|      | 视频                       | :heavy_check_mark: 王灏天90  |                              |                             |                             |
|      | 报告                       | :heavy_check_mark: 树畅90    | :heavy_check_mark: 熊汇雨30  | 褚进炜20                    |                             |