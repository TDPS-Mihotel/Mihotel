from controller import Robot

TIME_STEP = 64
robot = Robot()
#ds = []
#dsNames = ['ds_right', 'ds_left']
"""
for i in range(2):
    ds.append(robot.getDistanceSensor(dsNames[i]))
    ds[i].enable(TIME_STEP)
"""
wheels = []
wheelsNames = ['wheel1', 'wheel2', 'wheel3', 'wheel4']
for i in range(4):
    wheels.append(robot.getMotor(wheelsNames[i]))
    wheels[i].setPosition(float('inf'))
    wheels[i].setVelocity(0.0)
#avoidObstacleCounter = 0



    
def forward():
    leftSpeed = -1.0
    rightSpeed = -1.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)

def backward():
    leftSpeed = 1.0
    rightSpeed = 1.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)

def leftturn():
    leftSpeed = 1.0
    rightSpeed = -1.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)

def rightturn():
    leftSpeed = -1.0
    rightSpeed = 1.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)

def stop():
    leftSpeed = 0.0
    rightSpeed = 0.0
    wheels[0].setVelocity(leftSpeed)
    wheels[1].setVelocity(leftSpeed)
    wheels[2].setVelocity(rightSpeed)
    wheels[3].setVelocity(rightSpeed)

while robot.step(TIME_STEP) != -1:
    forward()