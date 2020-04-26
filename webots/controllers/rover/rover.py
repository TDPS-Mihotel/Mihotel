"""rover controller. This file should only be edited by Decision Group."""

import multiprocessing
import os
import sys
import time

# import chassis
# import detection
# TODO: fix colored module to use webots's AnsiCodes
# from colored import commandInfo, debugInfo, detectedInfo, info, logoInfo
from controller import Robot
from controller import AnsiCodes

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor


# flags ########################################################################
flag_patio_finished = 0


# initialize ###################################################################
# create the Robot instance.
robot = Robot()
# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())


# You should insert a getDevice-like function in order to get the
# instance of a device of the robot. Something like:
#  motor = robot.getMotor('motorname')
#  ds = robot.getDistanceSensor('dsname')
#  ds.enable(timestep)


# start
# logoInfo()

print("This is " + AnsiCodes.RED_FOREGROUND + "red" + AnsiCodes.RESET + "!")
# Main loop:
# - perform simulation steps until Webots is stopping the controller
while robot.step(timestep) != -1:
    # Read the sensors:
    # Enter here functions to read sensor data, like:
    #  val = ds.getValue()

    # Process sensor data here.

    # Enter here functions to send actuator commands, like:
    #  motor.setPosition(10.0)
    pass
