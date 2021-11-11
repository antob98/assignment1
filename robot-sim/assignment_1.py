from __future__ import print_function
import time
from sr.robot import *

"""
This is my solution for the first Research Track Assignment of the Robotics Engineering Master Course held at University of Genova in the year 2021/2022. To run this code, get in the correct directory from the shell and use the command:
	$ python2 run.py assignment_1.py
"""

'''Threshold for orientation control'''
a_th=2.0
'''Threshold for linear distance control'''
d_th=0.4

R = Robot()
""" instance of the class Robot"""

def drive(speed, seconds): #base function, provided by the standard robot documentation. We applied no changes to it.
    """
    Function for setting a linear velocity

    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed #since this is a ... robot, applying the same speed to both motors will result in the robot moving forward at that speed for "seconds" seconds.
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds): #base function, provided by the standard robot documentation. We applied no changes to it.
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed #applying opposite velocities to the two motors will make the robot turn in place for "seconds" seconds.
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

#here goes the code
'''this function allows the robot to find silver tokens present in front of it. 

Its angular range of vision is 360 normally, and you can manually set the distance at which he's able to recognize objects. We reduced its vision capabilities to a cone of "dist" lenght and angle limited between the desired ext1 and ext2 set. We did this so that we could avoid.

Whenever the robot sees silver tokens in its cone of vision, this function calculates which is the nearest one and returns its distance and orientation with respect to the robot. Otherwise, in case no silver tokens are detected in the cone, it returns -1.'''
def find_silver_token(ext1,ext2):
    dist=2
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_SILVER and ext1 <= token.rot_y <= ext2:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==2:
        return -1, -1
    else:
        return dist, rot_y


'''this function has the same structure as find_silver_token, but allows the robot to find the golden tokens that make up the perimeter of the circuit instead. 

This time, the distance is higher because we want to keep processing all possible golden tokens in the cone to always know where the nearest one is. The distance threshold that decides when the robot will react is, in fact not defined here, but later in the main loop of our code. 

This combination allows the robot to always know where is the nearest golden token in its surroundings, but also to act only when specifically needed.'''
def find_wall(ext1,ext2):
    dist=100
    for token in R.see():
        if token.dist < dist and token.info.marker_type is MARKER_TOKEN_GOLD and ext1 <= token.rot_y <= ext2:
            dist=token.dist
	    rot_y=token.rot_y
    if dist==100:
        return -1, -1
    else:
        return dist, rot_y

'''This function allows the robot to correctly orientate itself with respect to an object placed in the x,y position. We will use it to get near the silver tokens in the correct ofientation to allow the robot to grab them.'''       
def rot_funct(x,y):
    if y<-a_th: 
        print("turn left")
        turn(-2,0.5)
    elif y>a_th:
        print("turn right")
        turn(+2,0.5)
    else:
        print("moving!")
        drive(50,0.1)


'''Function that allows the robot to grab the token and leave it behind itself when it's ready to do so. The threshold for distance control that allows the class function "grab" to work is used in the main loop of our code.'''
def grab_if(b,c,d):
    print("found it")
    if R.grab():
        print("grabbed it")
        turn(30,2)
        R.release()
        turn(-30,2)
    else:
        print("can't grab it yet")


'''Function used to avoid obstacles (golden markers) and choose how to move based on the actual position and orientation of the robot with respect to the surrounding golden blocks.

- When the robot has near walls on both sides (is at an angle of the perimeter) it will choose to move left or right based on the nearest perceived distance from the opposite side. - If, instead, it has only obstacles on the left or on the right it will move in the opposite direction. 
- If the obstacle is perceived just in front, it will try to avoid it based on its relative orientation, trying to keep the same motion direction (counter-clockwise). 

However, there is a case in which it may not be able to keep the same direction: if the nearest perceived golden block is directly in its front, with 0 as relative orientation and the same perceived distance from the lateral walls, then it will always prioritize left movement (because there's no way to tell which would be a correct direction).'''
def move_funct(b,c,d):
    print("iceberg detected")
    if dest_sx!=-1 and dest_sx<2:
        if dest_dx!=-1 and dest_dx<2:
            print("surrounded!")
            if dest_dx>dest_sx:
                print("turn right!")
                turn(+15,1)
            elif dest_sx>=dest_dx:
                print("turn left!")
                turn(-15,1)
        else:
            print("forward+left: turn right!")
            turn(+15,1)
    
    elif dest_dx!=-1 and dest_dx<2:
        print("forward+right: turn left!")
        turn(-15,1)
    
    else:
        print("just forward!")
        if d<-a_th:
            print("avoiding collision: turn right")
            turn(+15,1)
        elif d>a_th:
            print("avoiding collision: turn left")
            turn(-15,1)
        elif -a_th<=d<0:
            print("iceberg in front! turn right!")
            turn(+15,1)
        else:
            print("iceberg in front! turn left!")
            turn(-15,1)


set_dist=0.8 #threshold for distance control for golden tokens
while 1:
    #the angles used to shape the frontal and lateral cones of vision of the robot were the result of multiple tests. These ones gave the best performance and reliability overall.
    c,d=find_wall(-40,40)
    a,b=find_silver_token(-40,40)
    dest_sx,rot_sx=find_wall(-105,-75)
    dest_dx,rot_dx=find_wall(75,105)
    
    #priorities and behaviour
    if c<set_dist: #priority is given to safety: 
    #the robot should always avoid obstacles first
        move_funct(b,c,d)
    elif a==-1:
        print("I can't see any silver token")
        drive(50,0.1)     
    elif a<d_th:
        grab_if(b,c,d)
    else:
        print("moving!")
        rot_funct(a,b)


