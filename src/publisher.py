#!/usr/bin/python
import rospy
from numpy import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
from turtlesim.srv import TeleportAbsolute
from std_srvs.srv import Empty
#Inititiate ros node
rospy.init_node('send_vel')
#Call service to center and align the turtle each time
rospy.wait_for_service('turtle1/teleport_absolute')
center = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
center(5.544445, 5.544445, 0.5)
#Call service to clear the turtle background
rospy.wait_for_service('clear')
clear = rospy.ServiceProxy('clear', Empty)
clear()
#Get the current system time
t1 = time.time()
#Set a private parameter T for the total time of run
rospy.set_param('~T',10)
def publisher():
    
    pub_v = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    #Sets the rate at which to publish in hz
    rate = rospy.Rate(100)
    
   
    while not rospy.is_shutdown():
        v_msg = Twist()
        #Get the value of the param T
        T = rospy.get_param('T')
        
        t=0
        #Loop runs till the time specified
        while t<T:
            t = time.time() - t1
            #Main code for the trajectory
            vx = 12*pi*cos(4*pi*t/T)/T
            vy = 6*pi*cos(2*pi*t/T)/T
            ax = (-48*pi**2*sin(4*pi*t/T))/T**2
            ay = (-12*pi**2*sin(2*pi*t/T))/T**2
            des_v = sqrt(vx**2 + vy**2)
            des_w = ((ay*vx)-(ax*vy))/((vx*vx)+(vy*vy))
            #Prepare the message for publishing
            v_msg.linear.x=des_v   
            v_msg.angular.z = des_w
            #Publish
            pub_v.publish(v_msg)
            rate.sleep()
        #Shutdown the node after the figure is complete
        rospy.signal_shutdown('hua')
       
   
      
        

    
if __name__ == '__main__':
    
    publisher()
    
