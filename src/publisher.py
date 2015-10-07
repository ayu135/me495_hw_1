#!/usr/bin/python
import rospy
from std_msgs.msg import String
from numpy import *
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
import time
import math
from turtlesim.srv import TeleportAbsolute
from std_srvs.srv import Empty
rospy.init_node('send_vel')

rospy.wait_for_service('turtle1/teleport_absolute')
center = rospy.ServiceProxy('turtle1/teleport_absolute', TeleportAbsolute)
rospy.wait_for_service('clear')
clear = rospy.ServiceProxy('clear', Empty)
clear()
center(5.544445, 5.544445, 0.5)
t1 = time.time()
rospy.set_param('~T',10)
def publisher():
    
    pub_v = rospy.Publisher('turtle1/cmd_vel', Twist, queue_size=10)
    
    rate = rospy.Rate(100)
    
   
    while not rospy.is_shutdown():
        v_msg = Twist()
        T = rospy.get_param('T')
        
        t=0
        while t<T:
            t = time.time() - t1
            vx = 12*pi*cos(4*pi*t/T)/T
            vy = 6*pi*cos(2*pi*t/T)/T
            ax = (-48*pi**2*sin(4*pi*t/T))/T**2
            ay = (-12*pi**2*sin(2*pi*t/T))/T**2
            des_v = sqrt(vx**2 + vy**2)
            
            des_w = ((ay*vx)-(ax*vy))/((vx*vx)+(vy*vy))
            v_msg.linear.x=des_v   
            v_msg.angular.z = des_w
            pub_v.publish(v_msg)
            # pub_h.publish(h_msg)
            # print "v_msg: "
            # print v_msg.linear.x

            rate.sleep()
        rospy.signal_shutdown('hua')
       
   
      
        
def listener():

    
    # rospy.Subscriber("usb_cam/image_raw", Image, callback)
    publisher()
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
if __name__ == '__main__':
    
    listener()
    
