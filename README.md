Conents of the Assingment_1 Repository:
==========================================

The contents of this repository delve into my own solution for the 1st graded assignment given to us in the Research Track class of the Robotics Engineering Master course held in Università degli Studi di Genova. The simulator I used has been provided to us by our professor, so if you are interested in the explaination of all its functionalities or want to know more about the built-in Robot API you can follow the specifications listed in [CarmineD8's Github Repository](https://github.com/CarmineD8/python_simulator), specifically in the branch "assignment".

Installing and running this code:
------------------------------------

To run this code, make sure you have installed Python 2.7, the pygame library, PyPyBox2D, and PyYAML, then simply clone all the contents of this repository in your own repository, go inside the correct folder (where the file assignment_1.py is contained) from the shell and write the command:  
> `python2 run.py assignment_1.py`.

If you haven't downloaded python2, you can do it from the shell in this way:

> `sudo apt install python2`

For other useful info on the simulator used to produce this code, or the installation of the other components required besides python to make it work, you can always refer to the original repository granted to us by our professor. The link to his repository has been already given in the previous paragraph.

## Objectives and Useful Info:

The code produced for this assignment is contained in the file *assignment_1.py* and has been carried out in python2. Other than that, we produced this README to explain its contents.  
The assignment was:  
> Write a python script for achieving this robot’s behaviour:  
> Constrantly drive the robot around the circuit in the counter-clockwise direction.  
> Avoid touching the golden boxes.  
> When the robot is close to a silver box, it should grab it and move it behind itself.

The code we produced handles all points of the assignment without any problems. There is to note, though, that because of the way we wrote it there is an extremely niche case in which the robot could "turn" to avoid a specific obstacle, inverting its trajectory in the given circuit. The specific case may happen when the robot goes straight into an angle at a perfect 45° angle, being exactly at the same distance from both lateral walls. This uncertainty of its course of actions derives from the fact that in this case it is impossible for the robot to determine where it has to go to remain in counter-clockwise motion without it knowing at every instant its current position and orientation with respect tp the specific circuit. This can be avoided using a different approach, described in the "*Possible Improvements*" section.

### Code Behaviour (pseudocode):

The robot keeps looping 8 separate checks, each leading to their own instructions. 
While looping:
- If a golden token is in the frontal cone, take its position and orientation. 
- If a silver token is in the frontal cone, take its position and orientation.
- If a golden token is in the left cone, take its position and orientation. 
- If a golden token is in the right cone, take its position and orientation.
- If a golden token the distance of the golden token in front is less than set_dist:  
___If there was a golden token in the left cone and its distance was less than 2:  
_____If there also was a golden token in the right cone and its distance was less than 2:  
_______If the distance of the right token was greater than the distance of the left token:  
_________Turn right.  
_______Else if the distance of the left token was greater than the distance of the right token:  
_________Turn left.  
_______Else:  
_________Turn right.  
_____Else if there was a golden token in the right cone and its distance was less than 2:  
_______Turn left.  
_____Else:  
_______If the orientation angle of the frontal token is lower than -a_th:  
_________Turn right.  
_______Else if the orientation angle of the frontal token is greater than a_th:  
_________Turn left.  
_______Else if the orientation angle of the frontal token is greater than or equal to -a_th and strictly lower than 0:  
_________Turn right.  
_______Else:  
_________Turn left.  
- Else if no silver token has been detected:  
___Drive forward.  
- Else if there was a silver token and its distance was less than d_th:  
___If you can grab it:  
_____Turn around, release it, then turn around again.  
___Else:  
_____print "can't grab it yet"  
- Else:  
___If the orientation angle of the token is lower than -a_th:  
_____Turn left.  
___If the orientation angle of the token is greater than a_th:  
_____Turn right.  
___Else:  
_____Drive forward.

#### Possible Improvements:

As we previously stated, there is one uncertainty in the robot's behaviour that could be improved upon.  
It is due to the nature of our coding: since we were specifically asked to build it with functions and types of instructions seen during the course, we didn't use all the characteristics of the robot written in the file containing its class definition. For this reason, even if the class robot provides the possibility to know the robot-instance's position and orientation at each time instant, we chose not to use them in our code.  
This creates a drawback: if the robot goes straight into a corner at a 45° angle, thus perceiving the same distance from both lateral walls, it will give priority to left-turning. If we are lucky, it will be the right choice to preserve counter-clockwise motion, but we cannot really know in advance when this will happen. When it does, the robot may change its moving direction and start moving clockwise (because maybe in that situation to keep moving counter-clockwise in the circuit it would've needed to go right).  
This issue, however, isn't a critical one (since the robot will keep avoiding golden tokens and grab silver ones without problems) and as far as we tested, given the configuration of this particular circuit, this inconvenience may very well never happen (it would be almost impossible for the robot to get in that perfect orientation), so we left the code as is.  
To solve this issue we recommend either:
1. making the robot loosely know the intended path (code it in a way that allows it to have a mental map of which direction should he choose if it finds itself in this predicament at any time, and force its choice), even if this would require drastic changes in the original code and many more lines of code (to the point where it may not be worth it).  
Using the robot's built-in class functionalities to take account of its position and orientation at each time instant may greatly lower the ammount of additional code, so you should do it.  
An easy way to solve it in this way would be fixing the starting position and  angle of the robot as standards for comparison, then checking (each time it finds itself in an angle) the relative position and orientation with respect to the standards: in this way you can know which direction should you choose to go based on your how the angle is placed and where you are in the circuit.
2. making the robot know where it came from in terms of direction and position (maybe by memorizing a certain number of previous positions in time at runtime) and base its choice on that (to avoid taking the same path twice, thus also diverting from its intended motion).  
However, this would tie the robot's correct behaviour to this particular circuit, limiting its potential for reuse. There is, in fact, no *"correct"* general choice for always going counter-clockwise in all possible circuits that present angles in their perimeter.




