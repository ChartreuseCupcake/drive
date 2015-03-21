# ------------------------------------------------------------------------
# Drive.py
# ------------------------------------------------------------------------
#
#  Alan Li written on March 17, 2015
# 
#  Waffle Revengeance
#
# ------------------------------------------------------------------------

from .ev3dev import LegoSensor, Motor
import time

#Sensor Init
colorL = ColorSensor(port=0)
colorR = ColorSensor(port=1)
gyro = ColorSensor(port=2)
ultrasonic = ColorSensor(port=3)
USAngle = 0
USDist = 360			#Absolute amount to turn US 360 degrees

#MotorInit
def init_motor(motor):
	print ("Initializing motor")
	motor.reset()
	motor.run_mode = 'forever'
	motor.stop_mode = Motor.STOP_MODE.BRAKE
	motor.regulation_mode = True
	motor.pulses_per_second_sp = 0
	motor.start()
	print ("Motor Initialized")
	return;

a = Motor(port=Motor.PORT.A)
b = Motor(port=Motor.PORT.B)
c = Motor(port=Motor.PORT.C)
init_motor(a)
init_motor(b)
init_motor(c)
a.pulses_per_second_sp = 2000
b.pulses_per_second_sp = 2000
c.pulses_per_second_sp = 2000
time.sleep(5)
a.pulses_per_second_sp = 0
b.pulses_per_second_sp = 0
c.pulses_per_second_sp = 0
defaultSpeed = 1000

"""
drivestate variable. -1 awaits next instruction, 0 turns left, 1 forward, 2 turns
right and 3 is park.
"""
driveState = 0

				

#Method to get Sensor Readings
def get_sensors():
	output = [colorL.color(), colorR.color(),
		gyro.ang_and_rate(),
		ultrasonic.dist_in()
	]
	return output

def get_left_color():
	return colorL.rgb()

def get_right_color():
	return colorR.rgb()

def get_gyro_angle():
	return gyro.ang()

def get_distance():
	return ultrasonic.dist_in()

#Method to turn
def pointTurn(angle):
	gyroStartAngle = gyro.ang()
	gyroCurrentAngle = gyroStartAngle
	while(abs(gyroCurrentAngle - gyroStartAngle) == angle):
		gyroCurrentAngle = gyro.ang()
		if(angle > 0):
			a.run_forever(defaultSpeed)
			b.run_forever(-defaultSpeed)
		else:
			a.run_forever(-defaultSpeed)
			b.run_forever(defaultSpeed)
	a.stop()
	b.stop()


#Method to drive forward
def driveFoward(speed):
	a.run_forever(speed)
	b.run_forever(speed)

#Method to drive a certain distance
def driveForwardDist(speed, dist):
	a.run_position_limited(dist, speed)
	b.run_position_limited(dist, speed)

def driveCorrection():
	if(colorL.color() == 'white'):
		speed = b.pulses_per_second_sp
		b.pulses_per_second_sp = speed*0.9
	elif(colorR.color() == 'white'):
		speed = a.pulses_per_second_sp
		a.pulses_per_second_sp = speed*0.9
	if(colorL.color() != 'white' and colorR.color() != 'white')
		driveForward(defaultSpeed)

#Method to transition
def redLineStraighten():
	if(colorL.color() == 'red'):
		a.stop()
		while(colorR.color() != 'red'):
			b.run_forever(defaultSpeed)
		b.stop()
	elif(colorR.color() == 'red'):
		b.stop()
		while(colorR.color() != 'red'):
			a.run_forever(defaultSpeed)
		a.stop()
	time.sleep(1)

def atRedLine():
	if(colorL.color() == 'red' or colorR.color() == 'red'):
		return True

def checkCollision():
	initialUSAngle = USAngle
	resetUSToZero()
	turnUS(135)
	for i in range(7):
		turnUS(-15*(i))
		if(ultrasonic.dist_cm >= 20):
			return True;
	return False


def hugWallR(color):
	if(colorR.color() == 'black'):
		speedL = a.pulses_per_second_sp
		if(speedL*1.05 <= defaultSpeed):
			a.pulses_per_second_sp = speedL*1.1
		speedR = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedR*0.95
	if(colorR.color() == color || colorR.color() == 'yellow'):
		speedR = b.pulses_per_second_sp
		if(speedR*1.05 <= defaultSpeed):
			b.pulses_per_second_sp = speedR*1.05
		speedL = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedL*0.95

def hugWallL(color):
	if(colorL.color() == 'black'):
		speedR = a.pulses_per_second_sp
		if(speedR*1.05 <= defaultSpeed):
			a.pulses_per_second_sp = speedR*1.1
		speedL = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedL*0.95
	if(colorL.color() == color || colorR.color() == 'yellow'):
		speedL = b.pulses_per_second_sp
		if(speedL*1.05 <= defaultSpeed):
			b.pulses_per_second_sp = speedL*1.05
		speedR = b.pulses_per_second_sp
		b.pulses_per_second_sp = speedR*0.95

def findPark():
	hugWallR('white')

	if(colorR.color() = 'blue'):
		a.stop()
		b.stop()
		time.sleep(4)
	canParked = scanPark()
	driveForward(defaultSpeed)
	while(canParked == False):
		if(colorR.color() == 'white'):
			canParked = scanPark()
		hugWallR('blue')
	a.stop()
	b.stop()
	park()
	return 1

def turnUS(angle):
	c.run_position_limited(100,(angle/360.0)*USDist)
	USAngle += angle
	if(USAngle < 0)
		USAngle += 360
	elif(USAngle > 360)
		USAngle -= 360

def resetUSToZero():
	if(USAngle != 0):
		if(USAngle > 180):
			turnUS(-(360-USAngle)
		else:
			turnUS(360-USAngle)

def scanPark():
	for i in range(6):
		turnUS(-15*(i+1))
		if(ultrasonic.dist_cm >= 20):
			return True;
	return False

def park():
	while(colorL.color() != 'blue'):
			b.run_forever(defaultSpeed)
		b.stop()
		driveForwardDist(1000,17)
		time.sleep(4)
		driveForwardDist(-1000,17)
		pointTurn(-90)

def exit():
	hugWallL('white')
	if(colorL.color() == 'red'):
		a.stop()
		b.stop()
		while(colorR.color() != 'red'):
				b.run_forever(defaultSpeed)
			b.stop()
			driveForwardDist(1000,17)
		sys.exit(0);

#Method to maintain the current drive state
def main(instructions):
	instruct = instructions.pop(0)
	driveForward(defaultSpeed)
	driveState = 1;
	while(len(instructions) != 0):
		if(instructions.get(0) == 'P'):
			driveState = 2
		if(instructions.get(0) == 'E'):
			driveState = 3
		if(driveState == 0):					#Red Line state
			redLineStraighten()
			rightOfWay = checkCollision()
			if(rightOfWay):
				driveForwardDist(defaultSpeed, 20)
				pointTurn(instruct)
				driveState = 1
		if(driveState == 1):					#Drive down lane state
			driveCorrection()
		if(driveState == 2):					#Park Lane state 		!!!!
			driveState = findPark()
		if(driveState == 3):					#Exit Lane state 		!!!!
			exit()


		if(atRedLine()):
			instruct = instructions.pop(0)
		else:
			driveState = 0;


				#0: at a node
					#pause
					#straighten up
						#both sensors are read
				#1: transition nodes
					#read instruction
					#follow instruction
				#2: drive to node
					#drive forward
						#stay on road



#		if(driveState == -1):
#			driveState = instructions.pop(0)
#		elif(driveState == 0):
#			redLine()
#			turnLeft()
#			driveState = -1
#		elif(driveState == 1):
#			redLine()
#			goStraight()
#			driveState = -1
#		elif(driveState == 2):
#			redLine()
#			turnRight()
#			driveState = -1
#		elif(driveState == 3):
#			park()
#			driveState = -1

nodePath = [-90,-90,-90,0,0,-90,0,-90,0,-90,-90,'P',0,0,0,0,0,0,0,-90,'P',-90,0,0,0,-90,0,'P',0,-90,-90,0,0,-90,0,'E'] #List of instructions
main(nodePath)